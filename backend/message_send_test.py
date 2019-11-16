#pylint: disable=missing-docstring
#pylint: disable=unused-variable
import pytest

from functions.auth_functions import auth_register
from functions.channel_functions import channels_create, channel_join
from functions.message_functions import message_send
from functions.data import reset_data, get_data

from functions.exceptions import ValueError, AccessError


####################### ASSUMPTIONS #####################
'''
All test assume that nothing (users/channels/reacts/messages) exist prior to testing
It is assumed that messages sent must be atleast one character long
'''

#Send a message from authorised_user to the channel specified by channel_id

######################## GLOBAL VARIABLES SETUP ######################
def setup():
    reset_data()
    data = get_data()
    user_dict1 = auth_register('steven@gmail.com', 'hello123', 'Steven', 'Lay')
    user1 = user_dict1['token']
    user_id1 = user_dict1['u_id']

    user_dict2 = auth_register('2steven@gmail.com', 'hello123', '2Steven', 'Lay')
    user2 = user_dict2['token']
    user_id2 = user_dict2['u_id']

    channel_dict1 = channels_create(user1, 'chat1', True)
    channel1 = channel_dict1['channel_id']

    channel_dict2 = channels_create(user1, 'chat2', True)
    channel2 = channel_dict2['channel_id']

    channel_join(user2, channel1)

    messagelist = data['messages']

    return user1, user_id1, user2, user_id2, channel1, channel2, messagelist
##########################    END SETUP   ########################


#Testing string 'hello'
def test_message_send_1():
    user1, user_id1, user2, user_id2, channel1, channel2, messagelist = setup()
    assert message_send(user1, channel1, 'hello') == {'message_id': messagelist[0]['message_id']}

#Testing special characters
def test_message_send_2():
    user1, user_id1, user2, user_id2, channel1, channel2, messagelist = setup()
    assert (message_send(user1, channel1, '!@#$%^&*()_+=') ==
            {'message_id': messagelist[0]['message_id']})

#Testing numbers
def test_message_send_3():
    user1, user_id1, user2, user_id2, channel1, channel2, messagelist = setup()
    assert (message_send(user1, channel1, '1234567890') ==
            {'message_id': messagelist[0]['message_id']})

#Testing mixture of characters,numbers,special characters
def test_message_send_4():
    user1, user_id1, user2, user_id2, channel1, channel2, messagelist = setup()
    assert (message_send(user1, channel2, 'HeLlo123!@#%') ==
            {'message_id': messagelist[0]['message_id']})

#Testing 999 character string
def test_message_send_5():
    user1, user_id1, user2, user_id2, channel1, channel2, messagelist = setup()
    assert message_send(user1, channel2, 999*'a') == {'message_id': messagelist[0]['message_id']}

#Testing 1000 character string
def test_message_send_6():
    user1, user_id1, user2, user_id2, channel1, channel2, messagelist = setup()
    assert message_send(user1, channel1, 1000*'a') == {'message_id': messagelist[0]['message_id']}

#Testing string 1001 character string
def test_message_send_7():
    user1, user_id1, user2, user_id2, channel1, channel2, messagelist = setup()
    with pytest.raises(ValueError):
        message_send(user1, channel1, 1001*'a')

#Testing string definitely > 1000 characters
def test_message_send_8():
    user1, user_id1, user2, user_id2, channel1, channel2, messagelist = setup()
    with pytest.raises(ValueError):
        message_send(user1, channel1, 5000*'a')

#Messaging non joined channel
def test_message_send_9():
    user1, user_id1, user2, user_id2, channel1, channel2, messagelist = setup()
    with pytest.raises(AccessError):
        message_send(user2, channel2, 'hello')

#Messaging invalid channel
def test_message_send_10():
    user1, user_id1, user2, user_id2, channel1, channel2, messagelist = setup()
    with pytest.raises(ValueError):
        message_send(user1, 42, 'hello')
