''' Pytest functions used to test `channel_removeowner()`'''
#pylint: disable=missing-docstring
#pylint: disable=unused-variable
import pytest

from functions.auth_functions import auth_register
from functions.channel_functions import channels_create, channel_join, \
    channel_addowner, channel_removeowner

from functions.data import reset_data, is_owner
from functions.exceptions import ValueError, AccessError

'''
####################### ASSUMPTIONS ######################
Assume can only demote an owner if they are already an owner and have joined the
channel previously
Assume "invalid channel id" means they have not joined the channel OR it has not been created yet
Assume cannot demote the ONLY owner of the channel since there would be no owner to promote others

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

# Testing demoting an owner from a wrong channel id
def test_channel_removeowner_1():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    channel_addowner(owner_token, channel_id, u_id)
    invalid_id = channel_id + 1
    with pytest.raises(ValueError):
        channel_removeowner(owner_token, invalid_id, u_id)

# Testing demoting a member that has not joined the channel yet
def test_channel_removeowner_2():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Channels Name", True)
    channel_id = channel['channel_id']
    with pytest.raises(ValueError):
        channel_removeowner(owner_token, channel_id, u_id)

# Testing demoting a member in a channel they have joined
def test_channel_removeowner_3():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Channels Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    with pytest.raises(ValueError):
        channel_removeowner(owner_token, channel_id, u_id)

# Testing demoting a member in a channel they have been demoted before
def test_channel_removeowner_4():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    channel_addowner(owner_token, channel_id, u_id)
    channel_removeowner(owner_token, channel_id, u_id)
    with pytest.raises(ValueError):
        channel_removeowner(owner_token, channel_id, u_id)

# Testing a member attempting to demote himself - has no authority
def test_channel_removeowner_5():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Channels Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    with pytest.raises(ValueError):
        channel_removeowner(u_token, channel_id, u_id)

# Testing a member attempting to demote an owner
def test_channel_removeowner_7():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Channels Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    with pytest.raises(AccessError):
        channel_removeowner(u_token, channel_id, owner_id)

# Testing a member attempting to demote another member - has no authority
def test_channel_removeowner_8():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Channels Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    # Creating a new member
    member_dict = auth_register("person2@gmail.com", "password", "person", "two")
    member_id = member_dict['u_id']
    member_token = member_dict['token']
    # End member setup
    channel_join(member_token, channel_id)
    with pytest.raises(ValueError):
        channel_removeowner(u_token, channel_id, member_id)

# Testing an owner demoting another owner under the right conditions
def test_channel_removeowner_9():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    channel_addowner(owner_token, channel_id, u_id)
    channel_removeowner(owner_token, channel_id, u_id)
    assert is_owner(u_id, channel_id) == 0
    assert is_owner(owner_id, channel_id) == 1     # Checking the owner has not been demoted as well

# Testing an owner can be demoted multiple times after being promoted again
def test_channel_removeowner_10():
    owner_token, owner_id, u_token, u_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    channel_addowner(owner_token, channel_id, u_id)
    assert is_owner(u_id, channel_id)
    channel_removeowner(owner_token, channel_id, u_id)
    assert is_owner(u_id, channel_id) == 0
    channel_addowner(owner_token, channel_id, u_id)
    assert is_owner(u_id, channel_id)
    channel_removeowner(owner_token, channel_id, u_id)
    assert is_owner(u_id, channel_id) == 0
