''' Pytest functions used to test `channel_addowner()`'''
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
Assume the person who created the channel is the owner and has authority to promote
others to owner as well
Assume that the u_id being promoted has already joined the channel but as a member
Assume "invalid channel id" means they have not joined the channel yet OR it has
not been created yet

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

    member_dict = auth_register("person2@gmail.com", "password", "person", "two")
    member_token = member_dict['token']
    member_id = member_dict['u_id']

    return owner_token, owner_id, u_token, u_id, member_token, member_id
##########################    END SETUP   ########################


# Testing promoting a user to a channel that has not been created yet
def test_channel_addowner_1():
    owner_token, owner_id, u_token, u_id, member_token, member_id = setup()
    with pytest.raises(ValueError):
        channel_addowner(owner_token, 1234, u_id)

# Testing promoting a user to the wrong channel id
def test_channel_addowner_2():
    owner_token, owner_id, u_token, u_id, member_token, member_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    invalid_id = channel_id + 1
    with pytest.raises(ValueError):
        channel_addowner(owner_token, invalid_id, u_id)

# Testing promoting a user in a channel id they have not joined yet
def test_channel_addowner_3():
    owner_token, owner_id, u_token, u_id, member_token, member_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    with pytest.raises(ValueError):
        channel_addowner(owner_token, channel_id, u_id)


# Testing promoting the original owner of the channel
def test_channel_addowner_4():
    owner_token, owner_id, u_token, u_id, member_token, member_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    with pytest.raises(ValueError):
        channel_addowner(owner_token, channel_id, owner_id)

# Testing promoting a member of the channel who has already been promoted before
def test_channel_addowner_5():
    owner_token, owner_id, u_token, u_id, member_token, member_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    channel_addowner(owner_token, channel_id, u_id)
    with pytest.raises(ValueError):
        channel_addowner(owner_token, channel_id, u_id)

# Testing promoting a member if the person conducting the action does not have authority
# e.g. promoting themself
def test_channel_addowner_6():
    owner_token, owner_id, u_token, u_id, member_token, member_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    with pytest.raises(AccessError):
        channel_addowner(u_token, channel_id, u_id)

# Testing promoting a member if the person conducting the action does not have authority
# e.g. member promoting another member
def test_channel_addowner_7():
    owner_token, owner_id, u_token, u_id, member_token, member_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)

    channel_join(member_token, channel_id)
    with pytest.raises(AccessError):
        channel_addowner(u_token, channel_id, member_id)

# Testing promoting a member to owner under correct conditions
def test_channel_addowner_8():
    owner_token, owner_id, u_token, u_id, member_token, member_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    channel_addowner(owner_token, channel_id, u_id)
    assert is_owner(u_id, channel_id)                              # Checking user is now owner

    channel_join(member_token, channel_id)
    assert is_owner(member_id, channel_id) == 0     # Checking not owner since did not get promoted

# Testing a user promoted by another owner can promote others too
def test_channel_addowner_9():
    owner_token, owner_id, u_token, u_id, member_token, member_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    channel_addowner(owner_token, channel_id, u_id)
    assert is_owner(u_id, channel_id)

    channel_join(member_token, channel_id)
    channel_addowner(u_token, channel_id, member_id)
    assert is_owner(member_id, channel_id)

# Testing a user can be promoted to owner again after being demoted
def test_channel_addowner_10():
    owner_token, owner_id, u_token, u_id, member_token, member_id = setup()
    channel = channels_create(owner_token, "Channel Name", True)
    channel_id = channel['channel_id']
    channel_join(u_token, channel_id)
    channel_addowner(owner_token, channel_id, u_id)
    assert is_owner(u_id, channel_id)
    channel_removeowner(owner_token, channel_id, u_id)
    assert is_owner(u_id, channel_id) == 0
    channel_addowner(owner_token, channel_id, u_id)
    assert is_owner(u_id, channel_id)
