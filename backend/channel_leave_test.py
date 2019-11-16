''' Pytest functions used to test `channel_leave()`'''
#pylint: disable=missing-docstring
#pylint: disable=unused-variable

import pytest

from functions.auth_functions import auth_register
from functions.channel_functions import channels_create, channel_join, channels_list, channel_leave

from functions.data import reset_data

from functions.exceptions import ValueError


'''
####################### ASSUMPTIONS ######################
Assume you need to have joined the channel first before leaving
Assume "Channel does not exist" means channels you have not joined yet OR
channel_id hasn't been created yet
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


# Leaving a channel that has not been created yet
def test_channel_leave_1():
    owner_token, owner_id, u_token, u_id = setup()
    with pytest.raises(ValueError):
        channel_leave(u_token, 1234)

# Leaving a channel that has been created but not joined
def test_channel_leave_2():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    with pytest.raises(ValueError):
        channel_leave(u_token, channel_id)

# Leaving a non-matching channel that been created and joined
def test_channel_leave_3():
    owner_token, owner_id, u_token, u_id = setup()
    channel1 = channels_create(owner_token, "Channel Name", True)
    channel_id1 = channel1['channel_id']
    channel_join(u_token, channel_id1)
    invalid_channel_id = channel_id1 + 1
    with pytest.raises(ValueError):
        channel_leave(u_token, invalid_channel_id)

# Leaving a channel that hasn't been joined
def test_channel_leave_4():
    owner_token, owner_id, u_token, u_id = setup()
    channel1 = channels_create(owner_token, "Channel Name", True)
    channel2 = channels_create(owner_token, "Second Channel", True)
    channel3 = channels_create(owner_token, "Third Channel", True)
    channel_id1 = channel1['channel_id']
    channel_id2 = channel2['channel_id']
    channel_id3 = channel3['channel_id']
    channel_join(u_token, channel_id1)
    channel_join(u_token, channel_id2)
    with pytest.raises(ValueError):
        channel_leave(u_token, channel_id3)


# Leaving an invalid channel not matching any from a list of joined channels
def test_channel_list_5():
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
    invalid_channel_id = channel_id1 + channel_id2 + channel_id3
    with pytest.raises(ValueError):
        channel_leave(u_token, invalid_channel_id)

# Leaving the only channel they have joined would return empty list
def test_channel_leave_6():
    owner_token, owner_id, u_token, u_id = setup()
    channel1 = channels_create(owner_token, "Channel Name", True)
    channel_id1 = channel1['channel_id']
    channel_join(u_token, channel_id1)
    channel_leave(u_token, channel_id1)
    assert(channels_list(u_token) == {
        'channels': []
    })

# Leaving a channel out of 2 already joined
def test_channel_leave_7():
    owner_token, owner_id, u_token, u_id = setup()
    channel1 = channels_create(owner_token, "Channel Name", True)
    channel2 = channels_create(owner_token, "Second Channel", True)
    channel_id1 = channel1['channel_id']
    channel_id2 = channel2['channel_id']
    channel_join(u_token, channel_id1)
    channel_join(u_token, channel_id2)
    channel_leave(u_token, channel_id1)
    assert(channels_list(u_token) == {
        'channels': [
            {'channel_id': channel_id2, 'name': "Second Channel"}
        ]
    })

# Leaving a channel out of 4 already joined
def test_channel_leave_8():
    owner_token, owner_id, u_token, u_id = setup()
    channel1 = channels_create(owner_token, "Channel Name", True)
    channel2 = channels_create(owner_token, "Second Channel", True)
    channel3 = channels_create(owner_token, "Third Channel", True)
    channel4 = channels_create(owner_token, "Fourth Channel", True)
    channel_id1 = channel1['channel_id']
    channel_id2 = channel2['channel_id']
    channel_id3 = channel3['channel_id']
    channel_id4 = channel4['channel_id']
    channel_join(u_token, channel_id1)
    channel_join(u_token, channel_id2)
    channel_join(u_token, channel_id3)
    channel_join(u_token, channel_id4)
    channel_leave(u_token, channel_id3)
    assert(channels_list(u_token) == {
        'channels': [
            {'channel_id': channel_id1, 'name': "Channel Name"},
            {'channel_id': channel_id2, 'name': "Second Channel"},
            {'channel_id': channel_id4, 'name': "Fourth Channel"}
        ]
    })
