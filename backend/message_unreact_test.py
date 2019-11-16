from functions.auth_functions import auth_register
from functions.channel_functions import channels_create, channel_join
from functions.message_functions import message_send, message_remove, message_react, message_unreact
from functions.data import *

from functions.exceptions import ValueError, AccessError

import pytest

'''
####################### ASSUMPTIONS #####################
All test assume that nothing (users/channels/reacts/messages) exist prior to testing
All test assume that user1 and user2 are normal users
It is assumed that messages sent must be atleast one character long
All test assume that reacts exist from react_id 0 -> react_id 50
'''

#Given a message within a channel the authorised user is part of, remove a "react" to that particular message


######################## GLOBAL VARIABLES SETUP ######################
def setup():
    reset_data()
    data = get_data()
    userDict1 = auth_register('steven@gmail.com', 'hello123', 'Steven', 'Lay')
    user1 = userDict1['token']
    user_id1 = userDict1['u_id']

    userDict2 = auth_register('steven2@gmail.com','hello123','Steven2','Lay')
    user2 = userDict2['token']
    user_id2 = userDict2['u_id']

    channelDict1 = channels_create(user1, 'chat1', True)
    channel1 = channelDict1['channel_id']

    channelDict2 = channels_create(user1, 'chat2', True)
    channel2 = channelDict2['channel_id']

    channel_join(user2,channel1)

    return data, user1, user_id1, user2, user_id2, channel1, channel2
##########################    END SETUP   ########################

#Testing user unreacting to a message he reacted to with same react_id (1,1)
def test_message_unreact_1():
    data, user1, user_id1, user2, user_id2, channel1, channel2 = setup()
    message_send(user1,channel1,'Testing ureacts on slackr')
    message_react(user1,1,1)
    assert message_unreact(user1,1,1) == {}
    messagedict = message_dict(1)
    assert len(messagedict['reacts'][0]['u_ids']) == 0


#Testing user unreacting to a message with invalid react_id (1,2)
def test_message_unreact_2():
    data, user1, user_id1, user2, user_id2, channel1, channel2 = setup()
    message_send(user1,channel1,'Unreacting with reacts that do not exist')
    message_react(user1,1,1)
    with pytest.raises(ValueError):
	    message_unreact(user1,1,2)

#Testing user unreacting to message that doesn't exist
def test_message_unreact_3():
    data, user1, user_id1, user2, user_id2, channel1, channel2 = setup()
    with pytest.raises(ValueError):
	    message_unreact(user1,1,1)

#Testing user2 unreacting message from user1 that doesn't contain a react
def test_message_unreact_4():
    data, user1, user_id1, user2, user_id2, channel1, channel2 = setup()
    message_send(user1,channel1,'how about if you do not have a react')
    message_send(user2,channel1,'let me try again')
    with pytest.raises(ValueError):
	    message_unreact(user2,1,1)
