''' Pytest functions used to test `channel_join()`'''
#pylint: disable=missing-docstring
#pylint: disable=unused-variable

import pytest

from functions.auth_functions import auth_register
from functions.channel_functions import channels_create, channel_join, channels_list
from functions.misc_functions import admin_userpermission_change

from functions.data import reset_data

from functions.exceptions import ValueError, AccessError



'''
####################### ASSUMPTIONS ######################
Assume you need to need to create a channel first before joining
Also you cannot join a channel you are already in
Assume "Channel does not exist" means channels you have already joined OR
channel_id hasn't been created yet

Admins are the very first person to sign up to slackr
Admin privileges cover all of slackr
Owners are the first person to create the channel
Owner privileges cover ONLY their channel created
'''

######################## BEGIN SETUP ######################
def setup():
    reset_data()
    owner_dict = auth_register("owner@gmail.com", "password", "owner", "privileges")
    owner_token = owner_dict['token']
    owner_id = owner_dict['u_id']

    user_dict = auth_register("person1@gmail.com", "password", "person", "one")
    u_token = user_dict['token']
    u_id = user_dict['u_id']

    return owner_token, owner_id, u_token, u_id
##########################    END SETUP   ########################

# Testing joining a channel that hasn't been created yet
def test_channel_join_1():
    owner_token, owner_id, u_token, u_id = setup()
    with pytest.raises(ValueError):
        channel_join(u_token, 1234)

# Testing joining a channel with a different id to one that has been created
def test_channel_join_2():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Name", True)
    channel_id = channel['channel_id']
    invalid_channel_id = channel_id + 1
    with pytest.raises(ValueError):
        channel_join(u_token, invalid_channel_id)

# Testing joining a channel you have already joined
def test_channel_join_3():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    with pytest.raises(ValueError):
        channel_join(u_token, channel_id)

# Testing joining a different channel id to a list of already created channels
def test_channel_join_4():
    owner_token, owner_id, u_token, u_id = setup()
    channel1 = channels_create(owner_token, "Channel Name", True)
    channel2 = channels_create(owner_token, "Second Channel", True)
    channel3 = channels_create(owner_token, "Third Channel", True)
    channel_id1 = channel1['channel_id']
    channel_id2 = channel2['channel_id']
    channel_id3 = channel3['channel_id']
    invalid_channel_id = channel_id1 + channel_id2 + channel_id3
    with pytest.raises(ValueError):
        channel_join(u_token, invalid_channel_id)

# Testing joining a channel already joined in a list of channels
def test_channel_join_5():
    owner_token, owner_id, u_token, u_id = setup()
    channel1 = channels_create(owner_token, "Channel Name", True)
    channel2 = channels_create(owner_token, "Second Channel", True)
    channel3 = channels_create(owner_token, "Third Channel", True)
    channel_id1 = channel1['channel_id']
    channel_id2 = channel2['channel_id']
    channel_id3 = channel3['channel_id']
    channel_join(u_token, channel_id1)
    channel_join(u_token, channel_id2)
    channel_join(u_token, channel_id3)
    with pytest.raises(ValueError):
        channel_join(u_token, channel_id2)

# Testing joining a single channel already created
def test_channel_join_6():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    assert(channels_list(u_token) == {
        'channels': [
            {'channel_id': channel_id, 'name': "Name"}
        ]
    })

# Testing joining only one channel out of a list of channels
def test_channel_join_7():
    owner_token, owner_id, u_token, u_id = setup()
    channel1 = channels_create(owner_token, "Channel Name", True)
    channel2 = channels_create(owner_token, "Second Channel", True)
    channel3 = channels_create(owner_token, "Third Channel", True)
    channel_id1 = channel1['channel_id']
    channel_id2 = channel2['channel_id']
    channel_id3 = channel3['channel_id']
    channel_join(u_token, channel_id2)
    assert(channels_list(u_token) == {
        'channels': [
            {'channel_id': channel_id2, 'name': "Second Channel"}
        ]
    })


# Testing joining multiple channels
def test_channel_join_8():
    owner_token, owner_id, u_token, u_id = setup()
    channel1 = channels_create(owner_token, "Channel Name", True)
    channel2 = channels_create(owner_token, "Second Channel", True)
    channel3 = channels_create(owner_token, "Third Channel", True)
    channel_id2 = channel2['channel_id']
    channel_id3 = channel3['channel_id']
    channel_join(u_token, channel_id2)
    channel_join(u_token, channel_id3)
    assert(channels_list(u_token) == {
        'channels': [
            {'channel_id': channel_id2, 'name': "Second Channel"},
            {'channel_id': channel_id3, 'name': "Third Channel"}
        ]
    })

# Testing joining all available channels
def test_channel_join_9():
    owner_token, owner_id, u_token, u_id = setup()
    channel1 = channels_create(owner_token, "Channel Name", True)
    channel2 = channels_create(owner_token, "Second Channel", True)
    channel3 = channels_create(owner_token, "Third Channel", True)
    channel_id1 = channel1['channel_id']
    channel_id2 = channel2['channel_id']
    channel_id3 = channel3['channel_id']
    channel_join(u_token, channel_id1)
    channel_join(u_token, channel_id2)
    channel_join(u_token, channel_id3)
    assert(channels_list(u_token) == {
        'channels': [
            {'channel_id': channel_id1, 'name': "Channel Name"},
            {'channel_id': channel_id2, 'name': "Second Channel"},
            {'channel_id': channel_id3, 'name': "Third Channel"}
        ]
    })

# Testing joining a private channel with no admin privileges
def test_channel_join_10():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Private Channel", False)
    channel_id = channel['channel_id']
    with pytest.raises(AccessError):
        channel_join(u_token, channel_id)

# Testing joining a private channel with admin privileges
def test_channel_join_11():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Private Channel", False)
    channel_id = channel['channel_id']
    admin_userpermission_change(owner_token, u_id, 2)
    channel_join(u_token, channel_id)
    assert(channels_list(u_token) == {
        'channels': [
            {'channel_id': channel_id, 'name': "Private Channel"}
        ]
    })

# Testing joining a private channel after already joined
def test_channel_join_12():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Private Channel", False)
    channel_id = channel['channel_id']
    admin_userpermission_change(owner_token, u_id, 2)
    channel_join(u_token, channel_id)
    with pytest.raises(ValueError):
        channel_join(u_token, channel_id)

# Testing joining a few different channels as an admin
def test_channel_join_13():
    owner_token, owner_id, u_token, u_id = setup()
    channel1 = channels_create(owner_token, "Channel Name", True)
    channel2 = channels_create(owner_token, "Second Channel", True)
    channel3 = channels_create(owner_token, "Third Channel", True)
    channel4 = channels_create(owner_token, "Private1", False)
    channel5 = channels_create(owner_token, "Private2", False)
    channel6 = channels_create(owner_token, "Private3", False)
    channel_id2 = channel2['channel_id']
    channel_id3 = channel3['channel_id']
    channel_id5 = channel5['channel_id']
    admin_userpermission_change(owner_token, u_id, 2)
    channel_join(u_token, channel_id2)
    channel_join(u_token, channel_id3)
    channel_join(u_token, channel_id5)
    assert(channels_list(u_token) == {
        'channels': [
            {'channel_id': channel_id2, 'name': "Second Channel"},
            {'channel_id': channel_id3, 'name': "Third Channel"},
            {'channel_id': channel_id5, 'name': "Private2"}
        ]
    })
