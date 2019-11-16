import pytest
from functions.auth_functions import auth_register, auth_logout
from functions.channel_functions import channels_create, channel_invite
from functions.data import reset_data, is_member

from functions.exceptions import ValueError, AccessError

#The only channels and users that exist are those created from
#this test. When you create a channel you join it.
######################## BEGIN SETUP ######################
def setup():
    reset_data()
    dict1 = auth_register('email1@gmail.com', 'validpass', 'Yasin', 'Kevin')
    token1 = dict1['token']
    u_id1 = dict1['u_id']

    dict2 = auth_register('email2@gmail.com', 'validpass', 'Peter', 'Steven')
    token2 = dict2['token']
    u_id2 = dict2['u_id']

    dict3 = auth_register('email3@gmail.com', 'validpass', 'Yasin', 'Peter')
    token3 = dict3['token']
    u_id3 = dict3['u_id']

    return token1, u_id1, token2, u_id2, token3, u_id3
##########################    END SETUP   ########################


#invite second user(member) to public channel created by first user(admin)
def test_channel_invite_test_1():
    token1, u_id1, token2, u_id2, token3, u_id3 = setup()
    channel = channels_create(token1, 'someChannel', 1)
    channel_id1 = channel['channel_id']

    assert(channel_invite(token1, channel_id1, u_id2) == {})
    assert(is_member(u_id2, channel_id1))


#invite first user(admin) to private channel created by second user(member)
def test_channel_invite_test_2():
    token1, u_id1, token2, u_id2, token3, u_id3 = setup()
    channel = channels_create(token2, 'someChannel', 0)
    channel_id1 = channel['channel_id']

    assert(channel_invite(token2, channel_id1, u_id1) == {})
    assert(is_member(u_id1, channel_id1))


#invite multiple people (2 users)
def test_channel_invite_test_3():
    token1, u_id1, token2, u_id2, token3, u_id3 = setup()
    channel = channels_create(token1, 'someChannel', 1)
    channel_id1 = channel['channel_id']

    assert(channel_invite(token1, channel_id1, u_id2) == {})
    assert(channel_invite(token1, channel_id1, u_id3) == {})

    assert(is_member(u_id2, channel_id1))
    assert(is_member(u_id3, channel_id1))

#inviting user to channel with a channel_id that does not exist i.e.
#(channel_id1 + channel_id2)
def test_channel_invite_test_4():
    token1, u_id1, token2, u_id2, token3, u_id3 = setup()
    channel1 = channels_create(token1, 'someChannel', 1)
    channel_id1 = channel1['channel_id']

    channel2 = channels_create(token1, 'someChannel2', 1)
    channel_id2 = channel2['channel_id']

    with pytest.raises(ValueError):
        channel_invite(token1, channel_id1 + channel_id2, u_id2)

#inviting user with user_id that does not exist (U_id1 + u_id2)
def test_channel_invite_test_5():
    token1, u_id1, token2, u_id2, token3, u_id3 = setup()
    channel1 = channels_create(token1, 'someChannel', 1)
    channel_id1 = channel1['channel_id']

    channel2 = channels_create(token1, 'someChannel2', 1)
    channel_id2 = channel2['channel_id']

    with pytest.raises(ValueError):
        channel_invite(token1, channel_id2, u_id1 + u_id2)

#both user_id and channel_id do not exist
def test_channel_invite_test_6():
    token1, u_id1, token2, u_id2, token3, u_id3 = setup()
    channel1 = channels_create(token1, 'someChannel', 1)
    channel_id1 = channel1['channel_id']

    channel2 = channels_create(token1, 'someChannel2', 1)
    channel_id2 = channel2['channel_id']

    with pytest.raises(ValueError):
        channel_invite(token1, channel_id1 + channel_id2, u_id1 + u_id2)



#user is already in the channel so cant invite himself
def test_channel_invite_test_7():
    token1, u_id1, token2, u_id2, token3, u_id3 = setup()
    channel = channels_create(token1, 'someChannel', 1)
    channel_id1 = channel['channel_id']

    with pytest.raises(ValueError):
        channel_invite(token1, channel_id1, u_id1)
