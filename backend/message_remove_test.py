#pylint: disable=missing-docstring
#pylint: disable=unused-variable
import pytest

from functions.auth_functions import auth_register
from functions.channel_functions import channels_create, channel_join
from functions.message_functions import message_send, message_remove
from functions.data import reset_data, user_dict, is_valid_message

from functions.exceptions import ValueError, AccessError

'''
####################### ASSUMPTIONS #####################
All test assume that nothing (users/channels/reacts/messages) exist prior to testing
All test assume that user1 is a normal user and admin1 and admin2 are admins
It is assumed that messages sent must be atleast one character long
It is assumed that the admin is logged in and any other messages are coming from
other users from different locations
'''

#Given a message_id for a message, this message is removed from the channel

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
    channel_join(admin2, channel1)

    return user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2
##########################    END SETUP   ########################


#Testing removing a message sent by an admin in a joined channel
def test_message_remove_1():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'testing 123')
    assert message_remove(admin1, 1) == {}
    assert not is_valid_message(1)

#Testing removing messages of messages with different ID's
def test_message_remove_2():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'test message one')
    message_send(admin1, channel1, 'test message two')
    assert message_remove(admin1, 1) == {}
    assert not is_valid_message(1)
    assert message_remove(admin1, 2) == {}
    assert not is_valid_message(2)

#Testing user removing another users message
def test_message_remove_3():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'sorry guys only admins can remove other peoples messages')
    message_send(user1, channel1, 'are you joking? let me test that')
    with pytest.raises(AccessError):
        message_remove(user1, 1)

#Testing admin trying to remove another persons message (in this case another admin)
def test_message_remove_4():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, "hey admin 2, apparently we can remove each others messages")
    message_send(admin2, channel1, 'that sounds pretty fair to me')
    assert message_remove(admin1, 2) == {}
    assert not is_valid_message(2)

#Testing admin trying to remove another persons message (in this case a users)
def test_message_remove_5():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(user1, channel1, "hey admin, did you hear you can remove other people messages")
    message_send(admin1, channel1, 'yep, let me show you my admin rights')
    assert message_remove(admin1, 1) == {}
    assert not is_valid_message(1)

#Testing an admin removing a message that was previously removed
def test_message_remove_6():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'Hello world!')
    message_remove(admin1, 1)
    with pytest.raises(ValueError):
        message_remove(admin1, 1)

#Testing an admin removing a message that doesn't exist
def test_message_remove_7():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    with pytest.raises(ValueError):
        message_remove(admin1, 1)

#Testing a user removing another users message
def test_message_remove_8():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'Hello world!')
    with pytest.raises(AccessError):
        message_remove(user1, 1)
