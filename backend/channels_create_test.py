''' Pytest functions used to test `channels_create()`'''
#pylint: disable=missing-docstring
#pylint: disable=unused-variable

import pytest

from functions.auth_functions import auth_register
from functions.channel_functions import channels_create

from functions.data import reset_data, channel_dict, decode_token
from functions.exceptions import ValueError

'''
####################### ASSUMPTIONS #####################
The name of a channel should be at least one character long - you can't name a channel nothing?
The channel ID will increase in number if created late
e.g. channel_id1 created first will be lower than the channel_id2 created last
'''


######################## BEGIN SETUP ######################
def setup():
    reset_data()
    owner_dict = auth_register("owner@gmail.com", "password", "owner", "privileges")
    owner_token = owner_dict['token']
    owner_id = owner_dict['u_id']

    return owner_token, owner_id
##########################    END SETUP   ########################


# Testing channel name that is exactly 21 characters long and is public
def test_channels_create_1():
    owner_token, owner_id = setup()
    with pytest.raises(ValueError):
        new_channel = channels_create(owner_token, "nameOfChannelIs21Long", True)

# Testing channel name that is exactly 21 characters long and isprivate
def test_channels_create_2():
    owner_token, owner_id = setup()
    with pytest.raises(ValueError):
        new_channel = channels_create(owner_token, "nameOfChannelIs21Long", False)

# Testing channel name that is significantly longer than 20 and public
def test_channels_create_3():
    owner_token, owner_id = setup()
    with pytest.raises(ValueError):
        new_channel = channels_create(owner_token, "nameOfChannelThatIsDefinitelyTooLong", True)

# Testing channel name that is significantly longer than 20 and private
def test_channels_create_4():
    owner_token, owner_id = setup()
    with pytest.raises(ValueError):
        new_channel = channels_create(owner_token, "nameOfChannelThatIsDefinitelyTooLong", False)

# Testing channel name that is exactly 20 characters long and Public
def test_channels_create_5():
    owner_token, owner_id = setup()
    new_channel = channels_create(owner_token, "nameOfChannelIs20xxx", True)
    channel_id = new_channel['channel_id']
    channel = channel_dict(channel_id)
    assert new_channel == {'channel_id': channel_id}
    assert(channel == {
        'channel_id': channel_id,
        'name': "nameOfChannelIs20xxx",
        'owner_members': [{
            'u_id': decode_token(owner_token),
        }],
        'all_members': [{
            'u_id': owner_id,
        }],
        'is_public': True,
        'messages': [],
        'standup_queue': [],
        'standup_active': False,
        'standup_end' : 0
    })

# Testing channel name that is exactly 20 characters long and Private
def test_channels_create_6():
    owner_token, owner_id = setup()
    new_channel = channels_create(owner_token, "nameOfChannelIs20xxx", False)
    channel_id = new_channel['channel_id']
    channel = channel_dict(channel_id)
    assert new_channel == {'channel_id': channel_id}
    assert(channel == {
        'channel_id': channel_id,
        'name': "nameOfChannelIs20xxx",
        'owner_members': [{
            'u_id': decode_token(owner_token),
        }],
        'all_members': [{
            'u_id': owner_id,
        }],
        'is_public': False,
        'messages': [],
        'standup_queue': [],
        'standup_active': False,
        'standup_end' : 0
    })

# Testing channel name that is exactly 19 characters long and Public
def test_channels_create_7():
    owner_token, owner_id = setup()
    new_channel = channels_create(owner_token, "nameOfChannelIs19xx", True)
    channel_id = new_channel['channel_id']
    channel = channel_dict(channel_id)
    assert new_channel == {'channel_id': channel_id}
    assert(channel == {
        'channel_id': channel_id,
        'name': "nameOfChannelIs19xx",
        'owner_members': [{
            'u_id': decode_token(owner_token),
        }],
        'all_members': [{
            'u_id': owner_id,
        }],
        'is_public': True,
        'messages': [],
        'standup_queue': [],
        'standup_active': False,
        'standup_end' : 0
    })

# Testing channel name that is exactly 19 characters long and Private
def test_channels_create_8():
    owner_token, owner_id = setup()
    new_channel = channels_create(owner_token, "nameOfChannelIs19xx", False)
    channel_id = new_channel['channel_id']
    channel = channel_dict(channel_id)
    assert new_channel == {'channel_id': channel_id}
    assert(channel == {
        'channel_id': channel_id,
        'name': "nameOfChannelIs19xx",
        'owner_members': [{
            'u_id': decode_token(owner_token),
        }],
        'all_members': [{
            'u_id': owner_id,
        }],
        'is_public': False,
        'messages': [],
        'standup_queue': [],
        'standup_active': False,
        'standup_end' : 0
    })

# Testing numbers count as a character
def test_channels_create_9():
    owner_token, owner_id = setup()
    new_channel = channels_create(owner_token, "123456789", True)
    channel_id = new_channel['channel_id']
    channel = channel_dict(channel_id)
    assert new_channel == {'channel_id': channel_id}
    assert(channel == {
        'channel_id': channel_id,
        'name': "123456789",
        'owner_members': [{
            'u_id': decode_token(owner_token),
        }],
        'all_members': [{
            'u_id': owner_id,
        }],
        'is_public': True,
        'messages': [],
        'standup_queue': [],
        'standup_active': False,
        'standup_end' : 0
    })

# Testing too many numbers will raise an error
def test_channels_create_10():
    owner_token, owner_id = setup()
    with pytest.raises(ValueError):
        new_channel = channels_create(owner_token, "1234567890123456789012345", True)

#T Testing symbols will count as a character
def test_channels_create_11():
    owner_token, owner_id = setup()
    new_channel = channels_create(owner_token, "~!@#$%^&*()_-+=", False)
    channel_id = new_channel['channel_id']
    channel = channel_dict(channel_id)
    assert new_channel == {'channel_id': channel_id}
    assert(channel == {
        'channel_id': channel_id,
        'name': "~!@#$%^&*()_-+=",
        'owner_members': [{
            'u_id': decode_token(owner_token),
        }],
        'all_members': [{
            'u_id': owner_id,
        }],
        'is_public': False,
        'messages': [],
        'standup_queue': [],
        'standup_active': False,
        'standup_end' : 0
    })

def test_channels_create_12():
    owner_token, owner_id = setup()
    new_channel = channels_create(owner_token, r"[]{}\|;:',./<>?", False)
    channel_id = new_channel['channel_id']
    channel = channel_dict(channel_id)
    assert new_channel == {'channel_id': channel_id}
    assert(channel == {
        'channel_id': channel_id,
        'name': r"[]{}\|;:',./<>?",
        'owner_members': [{
            'u_id': decode_token(owner_token),
        }],
        'all_members': [{
            'u_id': owner_id,
        }],
        'is_public': False,
        'messages': [],
        'standup_queue': [],
        'standup_active': False,
        'standup_end' : 0
    })

# Testing space bar counts as a character
def test_channels_create_13():
    owner_token, owner_id = setup()
    new_channel = channels_create(owner_token, "        ", True)
    channel_id = new_channel['channel_id']
    channel = channel_dict(channel_id)
    assert new_channel == {'channel_id': channel_id}
    assert(channel == {
        'channel_id': channel_id,
        'name': "        ",
        'owner_members': [{
            'u_id': decode_token(owner_token),
        }],
        'all_members': [{
            'u_id': owner_id,
        }],
        'is_public': True,
        'messages': [],
        'standup_queue': [],
        'standup_active': False,
        'standup_end' : 0
    })

# Testing too many symbols will create an error
def test_channels_create_14():
    owner_token, owner_id = setup()
    with pytest.raises(ValueError):
        new_channel = channels_create(owner_token, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", False)

# Testing a mix of letters and symbols
def test_channels_create_15():
    owner_token, owner_id = setup()
    new_channel = channels_create(owner_token, "name123!@#", True)
    channel_id = new_channel['channel_id']
    channel = channel_dict(channel_id)
    assert new_channel == {'channel_id': channel_id}
    assert(channel == {
        'channel_id': channel_id,
        'name': "name123!@#",
        'owner_members': [{
            'u_id': decode_token(owner_token),
        }],
        'all_members': [{
            'u_id': owner_id,
        }],
        'is_public': True,
        'messages': [],
        'standup_queue': [],
        'standup_active': False,
        'standup_end' : 0
    })

# Testing a long string of letters and symbols
def test_channels_create_16():
    owner_token, owner_id = setup()
    with pytest.raises(ValueError):
        new_channel = channels_create(owner_token, "VeryLongName123456!@#$%^@!#", True)

# Testing expected previous behaviour with a different token
def test_channels_create_17():
    owner_token, owner_id = setup()
    user_dict = auth_register("person_one@gmail.com", "password", "person", "one")
    different_token = user_dict['token']
    new_channel = channels_create(different_token, "Name123!@#", False)
    channel_id = new_channel['channel_id']
    channel = channel_dict(channel_id)
    assert new_channel == {'channel_id': channel_id}
    assert(channel == {
        'channel_id': channel_id,
        'name': "Name123!@#",
        'owner_members': [{
            'u_id': user_dict['u_id'],
        }],
        'all_members': [{
            'u_id': user_dict['u_id'],
        }],
        'is_public': False,
        'messages': [],
        'standup_queue': [],
        'standup_active': False,
        'standup_end' : 0
    })

# Testing long name with a different token
def test_channels_create_18():
    owner_token, owner_id = setup()
    user_dict = auth_register("person_two@gmail.com", "password", "person", "one")
    different_token = user_dict['token']
    with pytest.raises(ValueError):
        new_channel = channels_create(different_token, "VeryLongName123456!@#$^$", False)

# Testing creating multiple public channels - channel_id should be increasing order
def test_channels_create_19():
    owner_token, owner_id = setup()
    new_channel1 = channels_create(owner_token, "Channel 1", True)
    new_channel2 = channels_create(owner_token, "Channel 2", True)
    new_channel3 = channels_create(owner_token, "Channel 3", True)
    assert new_channel1 == {'channel_id': 1}
    assert new_channel2 == {'channel_id': 2}
    assert new_channel3 == {'channel_id': 3}

# Testing creating multiple private channels - channel_id should be increasing order
def test_channels_create_20():
    owner_token, owner_id = setup()
    new_channel1 = channels_create(owner_token, "Channel 1", False)
    new_channel2 = channels_create(owner_token, "Channel 2", False)
    new_channel3 = channels_create(owner_token, "Channel 3", False)
    assert new_channel1 == {'channel_id': 1}
    assert new_channel2 == {'channel_id': 2}
    assert new_channel3 == {'channel_id': 3}

# Testing creating multiple public & private channels - channel_id should be increasing order
def test_channels_create_21():
    owner_token, owner_id = setup()
    new_channel1 = channels_create(owner_token, "Channel 1", True)
    new_channel2 = channels_create(owner_token, "Channel 2", False)
    new_channel3 = channels_create(owner_token, "Channel 3", True)
    new_channel4 = channels_create(owner_token, "Channel 4", False)
    assert new_channel1 == {'channel_id': 1}
    assert new_channel2 == {'channel_id': 2}
    assert new_channel3 == {'channel_id': 3}
    assert new_channel4 == {'channel_id': 4}
