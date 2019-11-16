#pylint: disable=missing-docstring
#pylint: disable=unused-variable
import pytest

from functions.auth_functions import auth_register
from functions.channel_functions import channels_create, channel_join
from functions.message_functions import message_send, message_pin
from functions.data import reset_data, user_dict, message_dict

from functions.exceptions import ValueError, AccessError


'''
####################### ASSUMPTIONS #####################
All test assume that nothing (users/channels/reacts/messages) exist prior to testing
All test assume that user1 and user2 are normal users
It is assumed that messages sent must be atleast one character long
'''

#Given a message within a channel, mark it as "pinned"
#to be given special display treatment by the frontend

######################## BEGIN SETUP ######################
def setup():
    reset_data()
    user_dict1 = auth_register('steven@gmail.com', 'hello123', 'Steven', 'Lay')
    user1 = user_dict1['token']
    user_id1 = user_dict1['u_id']
    user = user_dict(user_id1)
    user['permission_id'] = 3

    admin_dict1 = auth_register('adminsteven@gmail.com', 'adminhello123', 'adminSteven', 'Lay')
    admin1 = admin_dict1['token']
    admin_id1 = admin_dict1['u_id']
    admin = user_dict(admin_id1)
    admin['permission_id'] = 1

    admin_dict2 = auth_register('admin2steven@gmail.com', 'adminhello123', 'adminSteven', 'Lay')
    admin2 = admin_dict2['token']
    admin_id2 = admin_dict2['u_id']
    admin_2 = user_dict(admin_id2)
    admin_2['permission_id'] = 1

    channel_dict1 = channels_create(admin1, 'chat1', True)
    channel1 = channel_dict1['channel_id']

    channel_dict2 = channels_create(user1, 'chat2', True)
    channel2 = channel_dict2['channel_id']

    channel_join(user1, channel1)

    return user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2
##########################    END SETUP   ########################


#Testing admin pinning own message
def test_message_pin_1():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'testing 123')
    assert message_pin(admin1, 1) == {}
    message_id = 1
    messagedict = message_dict(message_id)
    assert messagedict['is_pinned']

#Testing admin pinning another persons message (a users)
def test_message_pin_2():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(user1, channel1, 'could an admin pin this message, it is very important')
    assert message_pin(admin1, 1) == {}
    message_id = 1
    messagedict = message_dict(message_id)
    assert messagedict['is_pinned']

#Testing user pinning another persons message (an admins)
def test_message_pin_3():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'could a user pin this message for test purposes')
    with pytest.raises(ValueError):
        message_pin(user1, 1)

#Testing admin pinning an already pinned message
def test_message_pin_4():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'I wonder what happens if I pin my own message twice')
    message_pin(admin1, 1)
    with pytest.raises(ValueError):
        message_pin(admin1, 1)

#Testing admin pinning message that doesn't exist
def test_message_pin_5():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    with pytest.raises(ValueError):
        message_pin(admin1, 1)

#Member is not a part of channel
def test_message_pin_6():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'Test message')
    with pytest.raises(AccessError):
        message_pin(admin2, 1)
