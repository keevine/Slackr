#pylint: disable=missing-docstring
#pylint: disable=unused-variable
import datetime
import pytest

from functions.auth_functions import auth_register
from functions.channel_functions import channels_create, channel_join
from functions.message_functions import message_send, message_sendlater
from functions.data import reset_data, get_data, message_dict

from functions.exceptions import ValueError, AccessError


'''
####################### ASSUMPTIONS ######################
Assume "invalid channel id" means the channel has not been created yet OR user
hasn't joined the channel yet
Assume messages must be at least one character long
Assume time in the past means any time before the current time on the user's system
Assume can still use this feature to send messages with no delay
i.e. exactly the same as message_send()
'''


######################## GLOBAL VARIABLES SETUP ######################
def setup():
    reset_data()
    owner_dict = auth_register("owner@gmail.com", "password", "owner", "privileges")
    owner_token = owner_dict['token']
    owner_id = owner_dict['u_id']

    user_dict1 = auth_register("person1@gmail.com", "password", "person", "one")
    u_token = user_dict1['token']
    u_id = user_dict1['u_id']

    return owner_token, owner_id, u_token, u_id
##########################    END SETUP   ########################

# Testing sending a message in a channel which hasn't been created yet
def test_message_sendlater_1():
    owner_token, owner_id, u_token, u_id = setup()
    future_time = datetime.datetime(3000, 1, 1).timestamp()
    with pytest.raises(ValueError):
        message_sendlater(u_token, 1234, "message", future_time)

# Testing sending a message to an incorrect channel id
def test_message_sendlater_2():
    owner_token, owner_id, u_token, u_id = setup()
    future_time = datetime.datetime(3000, 1, 1).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    invalid_id = channel_id + 1
    with pytest.raises(ValueError):
        message_sendlater(u_token, invalid_id, "message", future_time)

# Testing sending a message to a channel that hasn't been joined yet
def test_message_sendlater_3():
    owner_token, owner_id, u_token, u_id = setup()
    future_time = datetime.datetime(3000, 1, 1).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    with pytest.raises(AccessError):
        message_sendlater(u_token, channel_id, "message", future_time)

# Testing sending a message that is more than 1000 characters long
def test_message_sendlater_4():
    owner_token, owner_id, u_token, u_id = setup()
    future_time = datetime.datetime(3000, 1, 1).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    with pytest.raises(ValueError):
        message_sendlater(u_token, channel_id, 1001 * "a", future_time)

# Testing sending a message exactly 1000 characters long should not raise an error
def test_message_sendlater_5():
    owner_token, owner_id, u_token, u_id = setup()
    future_time = datetime.datetime(3000, 1, 1).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    assert message_sendlater(u_token, channel_id, 1000 * "a", future_time) == {
        'message_id': 1
    }
    assert get_data()['messages'] == [{
        'message_id': 1,
        'u_id': u_id,
        'message': 1000 * "a",
        'time_created': future_time,
        'is_unread': True,
        'reacts': [],
        'is_pinned': False,
    }]

# Testing sending a message less than 1000 characters long
def test_message_sendlater_6():
    owner_token, owner_id, u_token, u_id = setup()
    future_time = datetime.datetime(3000, 1, 1).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    assert message_sendlater(u_token, channel_id, 999 * "a", future_time) == {
        'message_id': 1
    }
    assert get_data()['messages'] == [{
        'message_id': 1,
        'u_id': u_id,
        'message': 999 * "a",
        'time_created': future_time,
        'is_unread': True,
        'reacts': [],
        'is_pinned': False,
    }]

# Testing sending a message with numbers should not raise an error
def test_message_sendlater_7():
    owner_token, owner_id, u_token, u_id = setup()
    future_time = datetime.datetime(3000, 1, 1).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    assert message_sendlater(u_token, channel_id, "1234567890", future_time) == {
        'message_id': 1
    }
    assert get_data()['messages'] == [{
        'message_id': 1,
        'u_id': u_id,
        'message': "1234567890",
        'time_created': future_time,
        'is_unread': True,
        'reacts': [],
        'is_pinned': False,
    }]

# Testing sending a message with various symbols should not raise an error
def test_message_sendlater_8():
    owner_token, owner_id, u_token, u_id = setup()
    future_time = datetime.datetime(3000, 1, 1).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    assert (message_sendlater(u_token, channel_id, r"~!@#$%^&*()_+[]{}\|;:'',.<>/?", future_time)
            == {'message_id': 1})
    assert get_data()['messages'] == [{
        'message_id': 1,
        'u_id': u_id,
        'message': r"~!@#$%^&*()_+[]{}\|;:'',.<>/?",
        'time_created': future_time,
        'is_unread': True,
        'reacts': [],
        'is_pinned': False,
    }]

# Testing sending a message with too many symbols
def test_message_sendlater_9():
    owner_token, owner_id, u_token, u_id = setup()
    future_time = datetime.datetime(3000, 1, 1).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    with pytest.raises(ValueError):
        message_sendlater(u_token, channel_id, 1000 * "!@#$%", future_time)

# Testing sending a message immediately still raises error since it's not in future
def test_message_sendlater_10():
    owner_token, owner_id, u_token, u_id = setup()
    now_time = datetime.datetime.now().timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    with pytest.raises(ValueError):
        message_sendlater(u_token, channel_id, "Message", now_time)

# Testing sending a message a year in the past
def test_message_sendlater_11():
    owner_token, owner_id, u_token, u_id = setup()
    past_time = datetime.datetime(2018, 1, 1).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    with pytest.raises(ValueError):
        message_sendlater(u_token, channel_id, "Message", past_time)

# Testing sending a message one second into the past
def test_message_sendlater_12():
    owner_token, owner_id, u_token, u_id = setup()
    now = datetime.datetime.now()
    one_second_ago = (now - datetime.timedelta(seconds=1)).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    with pytest.raises(ValueError):
        message_sendlater(u_token, channel_id, "Message", one_second_ago)

# Testing sending a message an hour into the past
def test_message_sendlater_13():
    owner_token, owner_id, u_token, u_id = setup()
    now = datetime.datetime.now()
    one_hour_ago = (now - datetime.timedelta(hours=1)).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    with pytest.raises(ValueError):
        message_sendlater(u_token, channel_id, "Message", one_hour_ago)

# Testing under correct conditions - sending a test message one hour in the future
def test_message_sendlater_14():
    owner_token, owner_id, u_token, u_id = setup()
    now = datetime.datetime.now()
    one_hour_later = (now + datetime.timedelta(hours=1)).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    assert message_sendlater(u_token, channel_id, "Message", one_hour_later) == {
        'message_id': 1
    }
    assert get_data()['messages'] == [{
        'message_id': 1,
        'u_id': u_id,
        'message': "Message",
        'time_created': one_hour_later,
        'is_unread': True,
        'reacts': [],
        'is_pinned': False,
    }]

# Testing sending a test message one second in the future
def test_message_sendlater_15():
    owner_token, owner_id, u_token, u_id = setup()
    now = datetime.datetime.now()
    one_second_later = (now + datetime.timedelta(seconds=1)).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    assert message_sendlater(u_token, channel_id, "Message", one_second_later) == {
        'message_id': 1
    }
    assert get_data()['messages'] == [{
        'message_id': 1,
        'u_id': u_id,
        'message': "Message",
        'time_created': one_second_later,
        'is_unread': True,
        'reacts': [],
        'is_pinned': False,
    }]

# Testing sending multiple messages into the future
def test_message_sendlater_16():
    owner_token, owner_id, u_token, u_id = setup()
    now = datetime.datetime.now()
    one_hour_later = (now + datetime.timedelta(hours=1)).timestamp()
    two_hours_later = (now + datetime.timedelta(hours=2)).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    assert message_sendlater(u_token, channel_id, "Message One", one_hour_later) == {
        'message_id': 1
    }
    assert message_sendlater(u_token, channel_id, "Message Two", two_hours_later) == {
        'message_id': 2
    }
    assert get_data()['messages'] == [
        {
            'message_id': 1,
            'u_id': u_id,
            'message': "Message One",
            'time_created': one_hour_later,
            'is_unread': True,
            'reacts': [],
            'is_pinned': False,
        },
        {
            'message_id': 2,
            'u_id': u_id,
            'message': "Message Two",
            'time_created': two_hours_later,
            'is_unread': True,
            'reacts': [],
            'is_pinned': False,
        }
    ]

# Testing sending message into the future after sending one immediately
def test_message_sendlater_17():
    owner_token, owner_id, u_token, u_id = setup()
    now = datetime.datetime.now()
    one_hour_later = (now + datetime.timedelta(hours=1)).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    immediate_message = message_send(u_token, channel_id, "Immediate Message")
    assert message_sendlater(u_token, channel_id, "Future Message", one_hour_later) == {
        'message_id': 2
    }
    assert get_data()['messages'] == [
        message_dict(1),                    # from immediate message
        {
            'message_id': 2,
            'u_id': u_id,
            'message': "Future Message",
            'time_created': one_hour_later,
            'is_unread': True,
            'reacts': [],
            'is_pinned': False,
        }
    ]

# Testing sending message into the future before sending one immediately
def test_message_sendlater_18():
    owner_token, owner_id, u_token, u_id = setup()
    now = datetime.datetime.now()
    one_hour_later = (now + datetime.timedelta(hours=1)).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    assert message_sendlater(u_token, channel_id, "Future Message", one_hour_later) == {
        'message_id': 1
    }
    immediate_message = message_send(u_token, channel_id, "Immediate Message")
    assert get_data()['messages'] == [
        {
            'message_id': 1,
            'u_id': u_id,
            'message': "Future Message",
            'time_created': one_hour_later,
            'is_unread': True,
            'reacts': [],
            'is_pinned': False,
        },
        message_dict(2),                    # from immediate message
    ]

# Testing sending multiple messages immediately and in the future
def test_message_sendlater_19():
    owner_token, owner_id, u_token, u_id = setup()
    now = datetime.datetime.now()
    one_hour_later = (now + datetime.timedelta(hours=1)).timestamp()
    two_hours_later = (now + datetime.timedelta(hours=2)).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    assert message_sendlater(u_token, channel_id, "Future Message One", one_hour_later) == {
        'message_id': 1
    }
    immediate_message_1 = message_send(u_token, channel_id, "Immediate Message One")
    assert message_sendlater(u_token, channel_id, "Future Message Two", two_hours_later) == {
        'message_id': 3
    }
    immediate_message_2 = message_send(u_token, channel_id, "Immediate Message Two")
    assert get_data()['messages'] == [
        {
            'message_id': 1,
            'u_id': u_id,
            'message': "Future Message One",
            'time_created': one_hour_later,
            'is_unread': True,
            'reacts': [],
            'is_pinned': False,
        },
        message_dict(2),                    # from immediate message
        {
            'message_id': 3,
            'u_id': u_id,
            'message': "Future Message Two",
            'time_created': two_hours_later,
            'is_unread': True,
            'reacts': [],
            'is_pinned': False,
        },
        message_dict(4),                    # from immediate message
    ]

# Testing sending two messages into the future at the exact same time
def test_message_sendlater_20():
    owner_token, owner_id, u_token, u_id = setup()
    now = datetime.datetime.now()
    one_hour_later = (now + datetime.timedelta(hours=1)).timestamp()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    assert message_sendlater(u_token, channel_id, "Future Message One", one_hour_later) == {
        'message_id': 1
    }
    assert message_sendlater(u_token, channel_id, "Future Message Two", one_hour_later) == {
        'message_id': 2
    }
    assert get_data()['messages'] == [
        {
            'message_id': 1,
            'u_id': u_id,
            'message': "Future Message One",
            'time_created': one_hour_later,
            'is_unread': True,
            'reacts': [],
            'is_pinned': False,
        },
        {
            'message_id': 2,
            'u_id': u_id,
            'message': "Future Message Two",
            'time_created': one_hour_later,
            'is_unread': True,
            'reacts': [],
            'is_pinned': False,
        }
    ]
