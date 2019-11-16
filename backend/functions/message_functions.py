from datetime import datetime
from .exceptions import ValueError, AccessError
from .data import (get_data, get_channel_id, is_valid_channel,
                   is_valid_message, decode_token, is_member,
                   user_dict, react_dict, message_dict, remove_channel_message_dict,
                   message_insert)

#########################   MESSAGE FUNCTIONS  ###########################
def message_sendlater(token, channel_id, message, time_sent):
    #Initialising data from input
    data = get_data()
    #Valid channel error
    if not is_valid_channel(channel_id):
        raise ValueError('Channel ID is not a valid channel')
    #Message length error
    max_message_len = 1000
    if len(message) > max_message_len:
        raise ValueError('Message is more than 1000 characters')
    #Unauthorised user error
    u_id = decode_token(token)
    if not is_member(u_id, channel_id):
        raise AccessError('Authorised user has not joined the channel they are trying to post to')
    #The message_id will be 1 + length of messages
    message_id = 1 + len(data['messages'])
    #Past time error
    current_time = datetime.now().timestamp()
    if time_sent < current_time:
        raise ValueError('Time sent is a time in the past')
    #Message sendlater functionality
    new_message_dict = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_created': time_sent,
        'is_unread': True,
        'reacts': [],
        'is_pinned': False,
    }
    #Inserting message into the channel specific message list and into the global message list
    message_insert(channel_id, new_message_dict)
    return {'message_id': message_id}

def message_send(token, channel_id, message):
    #Initialising all data from input
    data = get_data()
    #Valid channel error
    if not is_valid_channel(channel_id):
        raise ValueError('Channel ID is not a valid channel')
    #Message length error
    max_message_len = 1000
    if len(message) > max_message_len:
        raise ValueError('Message is more than 1000 characters')
    #Unauthorised user error
    u_id = decode_token(token)
    if not is_member(u_id, channel_id):
        raise AccessError('Authorised user has not joined the channel they are trying to post to')
    #The message_id will be 1 + length of messages
    message_id = 1 + len(data['messages'])
    #Message send functionality
    current_time = datetime.now().timestamp()
    new_message_dict = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_created': current_time,
        'is_unread': True,
        'reacts': [],
        'is_pinned': False,
    }
    #Inserting message into the channel specific message list and into the global message list
    message_insert(channel_id, new_message_dict)
    return {'message_id': message_id}

def message_remove(token, message_id):
    #Initialising all data from input
    data = get_data()
    #Valid message error
    if not is_valid_message(message_id):
        raise ValueError('Message (based on ID) no longer exists')
    #Function setup: obtaining userdict and messagedict
    u_id = decode_token(token)
    userdict = user_dict(u_id)
    messagedict = message_dict(message_id)
    #Removing message from the global message list
    #User may remove their own message (u_id match) or admin/owners can remove
    #any message (permission != 3)
    if messagedict['u_id'] == u_id or userdict['permission_id'] != 3:
        data['messages'].remove(messagedict)
    else:
        raise AccessError('user is removing a message not of own')
    #Removing message from the channel specific message dict
    remove_channel_message_dict(message_id)
    return {}

def message_edit(token, message_id, message):
    #Message length error
    max_message_len = 1000
    if len(message) > max_message_len:
        raise ValueError('message is more than 1000 characters')
    #Valid message error
    if not is_valid_message(message_id):
        raise ValueError('Message (based on ID) no longer exists')
    #Function setup: obtaining userdict and messagedict
    u_id = decode_token(token)
    userdict = user_dict(u_id)
    messagedict = message_dict(message_id)
    #User may edit their own message (u_id match) or admin/owners can remove
    #any message (permission != 3)
    if messagedict['u_id'] == u_id or userdict['permission_id'] != 3:
        messagedict['message'] = message
    else:
        raise AccessError('user is editing a message not of own')
    return {}

def message_react(token, message_id, react_id):
    #Invalid message_id error
    if not is_valid_message(message_id):
        raise ValueError('message_id is not a valid message')
    #Invalid react_id error
    if react_id != 1:
        raise ValueError('react_id is not a valid React ID.')
    #Check if the message has react_dict already
    u_id = decode_token(token)
    messagedict = message_dict(message_id)
    #if react_id dict doesn't already exist for specific message
    if not any(d['react_id'] == react_id for d in messagedict['reacts']):
        new_react_dict = {
            'react_id': react_id,
            'u_ids': [u_id],
            'is_this_user_reacted': True
        }
        messagedict['reacts'].append(new_react_dict)
    #if the dict does already exist, append the u_id to it
    else:
        reactdict = react_dict(messagedict, react_id)
        if u_id not in reactdict['u_ids']:
            reactdict['u_ids'].append(u_id)
            reactdict['is_this_user_reacted'] = True
        else:
            raise ValueError('user has already reacted to this message')
    return {}

def message_unreact(token, message_id, react_id):
    u_id = decode_token(token)
    if not is_valid_message(message_id):
        raise ValueError('message_id is not a valid message')
    if react_id != 1:
        raise ValueError('react_id is not a valid React ID.')
    #Check if the message has react_dict already
    messagedict = message_dict(message_id)
    #if react_id dict doesn't already exist for specific message
    if not any(d['react_id'] == react_id for d in messagedict['reacts']):
        raise ValueError('message does not have this react_id')
    #if the dict does already exist, append the u_id to it
    reactdict = react_dict(messagedict, react_id)
    reactdict['u_ids'].remove(u_id)
    reactdict['is_this_user_reacted'] = False
    return {}

def message_pin(token, message_id):
    #Invalid message_id error
    if not is_valid_message(message_id):
        raise ValueError("Message ID is invalid")
    #checking if user is an admin
    u_id = decode_token(token)
    userdict = user_dict(u_id)
    #get channel_id
    channel_id = get_channel_id(message_id)
    if userdict['permission_id'] != 1:
        raise ValueError('user is not an admin')
    #Cycle through message list until id match and check wether it is already
    #pinned, if not pin it
    messagedict = message_dict(message_id)
    if not is_member(u_id, channel_id):
        raise AccessError('Authorised user has not joined the channel they are trying to pin to')
    if not messagedict['is_pinned']:
        messagedict['is_pinned'] = True
    else:
        raise ValueError('message is already pinned')
    return {}

def message_unpin(token, message_id):
    #check valid message
    if not is_valid_message(message_id):
        raise ValueError("Message ID is invalid")
    #checking if user is an admin
    u_id = decode_token(token)
    user = user_dict(u_id)
    messagedict = message_dict(message_id)
    #get channel_id
    channel_id = get_channel_id(message_id)
    if user['permission_id'] != 1:
        raise ValueError('user is not an admin')
    #Cycle through message list until id match and check wether it is
    #pinned, if it is unpin it
    if not is_member(u_id, channel_id):
        raise AccessError('Authorised user has not joined the channel they are trying to pin to')
    if messagedict['is_pinned']:
        messagedict['is_pinned'] = False
    else:
        raise ValueError("message isn't currently pinned")
    return {}
