from functions.auth_functions import auth_register
from functions.channel_functions import channels_create, channel_join, channels_list, channel_messages
from functions.message_functions import message_send, message_sendlater
from functions.misc_functions import admin_userpermission_change

from functions.data import *

import datetime
from functions.exceptions import ValueError, AccessError

import pytest

#Assuming there are 80 messages in the chat, since there is no function that
#returns the number of messages in the chat
#start must be atleast 0

######################## BEGIN SETUP ######################
def user_setup():
    reset_data()
    ownerDict = auth_register("owner@gmail.com", "password", "owner", "privileges")
    owner_token = ownerDict['token']
    owner_id = ownerDict['u_id']

    userDict = auth_register("person1@gmail.com", "password", "person", "one")
    u_token = userDict['token']
    u_id = userDict['u_id']

    channel_dict = channels_create(owner_token, 'channel name', True)
    channel_id = channel_dict['channel_id']

    channel_dict2 = channels_create(owner_token, 'channel 2', True)
    channel_id2 = channel_dict['channel_id']

    channel_join(u_token, channel_id)

    return owner_token, owner_id, u_token, u_id, channel_id, channel_id2

def message_setup():
    data = get_data()
    owner_token, owner_id, u_token, u_id, channel_id, channel_id2 = user_setup()
    
    # Loop through and add 52 messages to the message list
    for i in range(52):
        message_text = "message" + str(i)
        message = m1 = message_send(owner_token, channel_id, message_text)

    messagelist = data['messages']
    messagelist.sort(key = lambda i: i['time_created'],reverse=True)

    return messagelist
##########################    END SETUP   ########################


#different cases where the user should be able to view the message

#edge case, view from most recent message
def test_channel_messages_1():
    owner_token, owner_id, u_token, u_id, channel_id, channel_id2 = user_setup()
    messagelist = message_setup()

    list1 = []
    start = 0
    end = start + 50
    for i in range(start, end):
        list1.append(messagelist[i])
    assert(channel_messages(owner_token, channel_id, 0) == {
        'messages': list1,
        'start': 0,
        'end': 50,
    })

#Viewing from 2nd message in
def test_channel_messages_2():
    owner_token, owner_id, u_token, u_id, channel_id, channel_id2 = user_setup()
    messagelist = message_setup()

    list1 = []
    start = 2
    end = start + 50
    for i in range(start, end):
        list1.append(messagelist[i])
    assert(channel_messages(owner_token, channel_id, 2) == {
        'messages': list1,
        'start': 2,
        'end': 52,
    })

#view from  middle messages (overflow)
def test_channel_messages_3():
    owner_token, owner_id, u_token, u_id, channel_id, channel_id2 = user_setup()
    messagelist = message_setup()

    list1 = []
    start = 25
    end = 52
    for i in range(start, end):
        list1.append(messagelist[i])
    assert (channel_messages(owner_token, channel_id, 25) == {
        'messages': list1,
        'start': 25,
        'end': -1
    })

#view from out of index
def test_channel_messages_4():
    owner_token, owner_id, u_token, u_id, channel_id, channel_id2 = user_setup()
    messagelist = message_setup()

    list1 = []
    start = 53
    with pytest.raises(ValueError):
        channel_messages(owner_token, channel_id, 53)

#Testing invalid channel
def test_channel_messages_5():
    owner_token, owner_id, u_token, u_id, channel_id, channel_id2 = user_setup()
    messagelist = message_setup()

    list1 = []
    start = 0
    end = start + 50
    for i in range(start, end):
        list1.append(messagelist[i])
    with pytest.raises(ValueError):
        channel_messages(owner_token, 3, 0)

#Testing channel member not a part of
def test_channel_messages_6():
    owner_token, owner_id, u_token, u_id, channel_id, channel_id2 = user_setup()
    messagelist = message_setup()

    list1 = []
    start = 0
    end = start + 50
    for i in range(start, end):
        list1.append(messagelist[i])
    with pytest.raises(AccessError):
        channel_messages(u_token, 2, 0)

#Testing sendlater messages
def test_channel_messages_7():
    data = get_data()
    owner_token, owner_id, u_token, u_id, channel_id, channel_id2 = user_setup()

    now = datetime.datetime.now()
    one_hour_later = (now + datetime.timedelta(hours = 1)).timestamp()

    m1 = message_send(owner_token, channel_id, "message1")
    m2 = message_send(owner_token, channel_id, "message2")
    m3 = message_send(owner_token, channel_id, "message3")
    m4 = message_send(owner_token, channel_id, "message4")
    m5 = message_sendlater(owner_token, channel_id, "message5 (future)", one_hour_later)
    m6 = message_send(owner_token, channel_id, "message6")

    messagelist = data['messages']
    messagelist.sort(key = lambda i: i['time_created'],reverse=True)
    ##########################    END SETUP   ########################

    list1 = []
    start = 0
    end = 6
    timestamp = datetime.datetime.now().timestamp()
    for i in range(start, end):
        if timestamp > messagelist[i]['time_created']:
            list1.append(messagelist[i])
    assert (channel_messages(owner_token, channel_id, 0) == {
        'messages': list1,
        'start': 0,
        'end': -1
    })
