#pylint: disable=missing-docstring
#pylint: disable=unused-variable
#pylint: disable=too-many-locals
import pytest

from functions.auth_functions import auth_register
from functions.channel_functions import channels_create, channel_join
from functions.message_functions import message_send, message_remove, message_edit
from functions.data import reset_data, user_dict, message_dict, get_data

from functions.exceptions import ValueError, AccessError


'''
####################### ASSUMPTIONS #####################
All test assume that nothing (users/channels/reacts/messages) exist prior to testing
All test assume that user1 is a normal user and admin1 and admin2 are admins
It is assumed that messages sent must be atleast one character long
It is assumed that the admin is logged in and any other messages are coming from
other users from different locations
'''

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
    admin['permission_id'] = 2

    admin_dict2 = auth_register('admin2steven@gmail.com', 'adminhello123', 'adminSteven', 'Lay')
    admin2 = admin_dict2['token']
    admin_id2 = admin_dict2['u_id']
    admin_2 = user_dict(admin_id2)
    admin_2['permission_id'] = 2

    channel_dict1 = channels_create(admin1, 'chat1', 'true')
    channel1 = channel_dict1['channel_id']

    channel_dict2 = channels_create(user1, 'chat2', 'true')
    channel2 = channel_dict2['channel_id']

    channel_join(user1, channel1)
    channel_join(admin2, channel1)

    return user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2
##########################    END SETUP   ########################

#Testing editing a message sent from an admin
def test_message_edit_1():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'testing 123')
    assert message_edit(admin1, 1, 'new message') == {}
    message_id = 1
    messagedict = message_dict(message_id)
    assert messagedict['message'] == 'new message'

#Testing user attempting to edit other peoples messages
def test_message_edit_2():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'sorry guys only admins can edit other messages')
    message_send(user1, channel1, 'are you joking? let me test that')
    with pytest.raises(AccessError):
        message_edit(user1, 1, 'testing')

#Testing admin trying to edit another persons message (in this case an admins)
def test_message_edit_3():
    data = get_data()
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, "hey admin 2, apparently we can edit each others messages")
    message_send(admin2, channel1, 'that sounds pretty standard to me')
    assert message_edit(admin1, 2, 'admin1 is really cool') == {}
    for messagedict in data['messages']:
        if messagedict['message_id'] == 2:
            assert messagedict['message'] == 'admin1 is really cool'

#Testing admin trying to edit another persons message (in this case a users)
def test_message_edit_4():
    data = get_data()
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(user1, channel1, "hey admin, did you hear you can edit other people messages")
    message_send(admin1, channel1, 'yep, let me show you my admin rights')
    assert message_edit(admin1, 1, 'imagine not being an admin') == {}
    for messagedict in data['messages']:
        if messagedict['message_id'] == 1:
            assert messagedict['message'] == 'imagine not being an admin'

#Testing editing a message that doesn't exist
def test_message_edit_5():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    with pytest.raises(ValueError):
        message_edit(admin1, 1, 'hello')

#Testing editing a message that has been removed
def test_message_edit_6():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'testing')
    message_remove(admin1, 1)
    with pytest.raises(ValueError):
        message_edit(admin1, 1, 'hello world')

#Testing a user editing another users message
def test_message_edit_7():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'testing')
    with pytest.raises(AccessError):
        message_edit(user1, 1, 'hello world')

#Testing a user editing a message to a length > 1000
def test_message_edit_8():
    user1, user_id1, admin1, admin_id1, admin2, admin_id2, channel1, channel2 = setup()
    message_send(admin1, channel1, 'testing')
    with pytest.raises(ValueError):
        message_edit(admin1, 1, 1001*'a')
