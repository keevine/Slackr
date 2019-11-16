'''Implementation of channel functions used for the backend of Slackr Web Server'''

from datetime import datetime
from .data import get_data, user_dict, channel_dict, decode_token, is_member, is_owner, is_valid_channel
from .exceptions import ValueError, AccessError

# Create a channel by generating a new dictionary with all the neccessary info
# to be edited later by other functions
def channels_create(token, name, is_public):
    if len(name) > 20:
        raise ValueError("Name of channel is longer than 20 characters")
    data = get_data()
    owner_id = decode_token(token)
    # Give the channel an ID which corresponds to the number created e.g. 1st channel is ID1 ...
    new_channel_id = len(data['channels']) + 1
    # Create a dictionary with all the relevant info and append to data
    info_dict = {
        'channel_id': new_channel_id,
        'name': name,
        'owner_members': [{
            'u_id': owner_id,
        }],
        'all_members': [{
            'u_id': owner_id,
        }],
        'is_public': is_public,
        'messages': [],
        'standup_queue': [],
        'standup_active': False,
        'standup_end' : 0
    }
    data['channels'].append(info_dict)
    return {'channel_id': new_channel_id}

# Provide a list of all channels
def channels_listall(token):
    data = get_data()
    channel_list = []
    for channels in data['channels']:
        channel_list.append({
            'channel_id': channels['channel_id'],
            'name': channels['name']
        })
    return {'channels': channel_list}

# Provide a list of all channels the user has curently joined
def channels_list(token):
    data = get_data()
    u_id = decode_token(token)
    channel_list = []
    for channels in data['channels']:
        if is_member(u_id, channels['channel_id']):
            channel_list.append({
                'channel_id': channels['channel_id'],
                'name': channels['name']
            })
    return  {'channels': channel_list}

# Remove user data from both owner and member lists
def channel_leave(token, channel_id):
    u_id = decode_token(token)
    if not is_valid_channel(channel_id):
        raise ValueError(f"Channel ID: {channel_id} is invalid")
    if not is_member(u_id, channel_id):
        raise ValueError(f"User: {u_id} has not joined channel: {channel_id} yet")

    remove_from_list(u_id, channel_id, 'owner_members')
    remove_from_list(u_id, channel_id, 'all_members')
    return {}

# Add user data to a database of channel owners
def channel_addowner(token, channel_id, u_id):
    if not is_valid_channel(channel_id):
        raise ValueError(f"Channel ID: {channel_id} is invalid")
    if is_owner(u_id, channel_id):                         # Check if user getting promoted is owner
        raise ValueError(f"User: {u_id} is already an owner")
    if not is_owner(decode_token(token), channel_id):      # Check if user promoting is not an owner
        raise AccessError(f"User: {decode_token(token)} does not have privileges to promote others")
    if not is_member(u_id, channel_id):
        raise ValueError(f"User {u_id} has not joined channel: {channel_id} yet")

    channel = channel_dict(channel_id)
    # append user to list of owners
    channel['owner_members'].append({'u_id' : u_id})
    return {}

# Remove user data from a database of channel owners
def channel_removeowner(token, channel_id, u_id):
    if not is_valid_channel(channel_id):
        raise ValueError(f"Channel ID: {channel_id} is invalid")
    if not is_owner(u_id, channel_id):               # Check if user getting demoted is not an owner
        raise ValueError(f"User: {u_id} is not an owner")
    if not is_owner(decode_token(token), channel_id):      # Check if user promoting is not an owner
        raise AccessError(f"User: {decode_token(token)} does not have privileges to demote others")

    remove_from_list(u_id, channel_id, 'owner_members')
    return {}

# Invite another user to the current channel
def channel_invite(token, channel_id, u_id):
    inviter_u_id = decode_token(token)
    if u_id == inviter_u_id:
        raise ValueError(f"User: {u_id} cannot invite self")

    user_join(u_id, channel_id)
    return {}

# Join a channel by adding their user data to the channel database
def channel_join(token, channel_id):
    u_id = decode_token(token)
    user_join(u_id, channel_id)
    return {}

# Provide info on channel name, and who has joined the channel
def channel_details(token, channel_id):
    if not is_valid_channel(channel_id):
        raise ValueError(f"Channel ID: {channel_id} does not exist")
    if not is_member(decode_token(token), channel_id):
        raise AccessError(f"User: {decode_token(token)} is not a member of channel: {channel_id}")

    channel = channel_dict(channel_id)
    #transform list into dictionary with relevant information for output
    owner_details = generate_dict(channel['owner_members'])
    all_details = generate_dict(channel['all_members'])

    details = {
        'name' : channel['name'],
        'owner_members' : owner_details,
        'all_members' : all_details
    }
    return details

# Display messages sent to the channel
def channel_messages(token, channel_id, start):
    data = get_data()
    #Checking channel_id is valid
    if not is_valid_channel(channel_id):
        raise ValueError(f"Invalid channel ID: {channel_id}")
    #Checking length of messages
    channeldict = channel_dict(channel_id)
    if(start > len(channeldict['messages'])):
        raise ValueError(f"Start index: {start} is greater than the amount of messages")
    #Checking if user is authorised in correct channel
    u_id = decode_token(token)
    if(is_member(u_id, channel_id) == False):
        raise AccessError(f"User: {u_id} is not a member of channel: {channel_id}")
    #Update React Status
    update_react_status(u_id)
    #Channel messages setup
    display_message_list = []
    end = start + 50
    if end > len(channeldict['messages']):
        endindex = len(channeldict['messages'])
        end = -1
    else:
        endindex = end
    timestamp = datetime.now().timestamp()
    #Channel messages functionality
    for message in range(start,endindex):
        #Check if the current time is > then the time the message is created
        if timestamp > channeldict['messages'][message]['time_created']:
            #If it is, it gets appended to a 'display list'
            display_message_list.append(channeldict['messages'][message])
    channeldict['messages'].sort(key = lambda i: i['time_created'],reverse=True)
    return {'messages': display_message_list, 'start': start, 'end': end,}

    #given start return end which is start + 50 or -1 if theres no more messages

######################  HELPER FUNCTIONS  ########################

# Add user info to the global data base
def user_join(u_id, channel_id):
    user = user_dict(u_id)
    channel = channel_dict(channel_id)

    if user == None: #check user exists
        raise ValueError(f"User ID: {u_id} does not exist")
    if channel == None: #check channel exists
        raise ValueError(f"Channel ID: {channel_id} does not exist")

    if is_member(u_id, channel_id): #verify user not already part of channel
        raise ValueError(f"User: {u_id} has already joined channel: {channel_id}")


    #validate users pemission before joining as member/owner
    MEMBER = 3
    if user['permission_id'] != MEMBER:
        channel['owner_members'].append({
            'u_id' : u_id
        })
        channel['all_members'].append({
            'u_id' : u_id
        })
    elif user['permission_id'] == MEMBER and channel['is_public']:
        channel['all_members'].append({
            'u_id' : u_id
        })
    else:
        raise AccessError(f"User: {u_id} is not authorised to join private channel: {channel_id}")

# Create a dictionary from a list of members containing information on their profile
def generate_dict(member_list):
    list = []
    for dict in member_list:
        user = user_dict(dict['u_id'])      # extract u_id from list of dictionaries
        name_dict = {
            'u_id' : user['u_id'],
            'name_first' : user['name_first'],
            'name_last' : user['name_last'],
            'profile_img_url' : user['profile_img_url']
        }
        list.append(name_dict)
    return list

# Helper function used in channel leave and removeowner
# Loops through data list and removes users from the owner or member list
def remove_from_list(u_id, channel_id, member_type):
    channel = channel_dict(channel_id)
    for member in channel[member_type]:
        if member['u_id'] == u_id:
            channel[member_type].remove(member)

# Helper function used in channel messages
# Loops through react dicts in message list and updates status of reacts          
def update_react_status(u_id):
    data = get_data()
    for message in data['messages']:
        for react in message['reacts']:
            if u_id not in react['u_ids']:
                react['is_this_user_reacted'] = False
            else:
                react['is_this_user_reacted'] = True
