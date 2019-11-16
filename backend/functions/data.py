#pylint: disable=missing-docstring
import hashlib
import re
import time
from json import dumps
#from flask import Flask, request, jsonify
#from flask_mail import Mail, Message
import jwt
#import copy
#import urllib.request
#from random import randint
#from werkzeug.exceptions import HTTPException
#from PIL import Image
from .exceptions import ValueError, AccessError

#GLOBAL VARIABLES
REGEX = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
SECRET = "daenerys"
DATA = {
    'users' : [],
    'channels' : [],
    'messages' : []
}

########################    HELPER FUNCTIONS    #########################

# Check if email is valid
def valid_email(email):
    return bool(re.search(REGEX, email))

# Abstraction for returning global data
def get_data():
    global DATA
    return DATA

# Abstraction for returning json string
def send(data):
    return dumps(data)

# Encodes token given string and SECRET
def generate_token(string):
    global SECRET
    return jwt.encode(
        {'string' : string, 'time' : time.time()},
        SECRET, algorithm='HS256').decode('utf-8')

# Decodes token given string and SECRET
def decode_token(token):
    global SECRET
    decoded = jwt.decode(token.encode('utf-8'), SECRET, algorithms=['HS256'])
    return decoded['string']

# Obtains channel_id from message_id
def get_channel_id(message_id):
    data = get_data()
    channels = data['channels']
    for channeldict in channels:
        messagelist = channeldict['messages']
        for messagedict in messagelist:
            if messagedict['message_id'] == message_id:
                channel_id = channeldict['channel_id']
                return channel_id
    return None

# Generates hash for string
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Return Bool value if user is logged in based on token
def is_logged_in(token):
    u_id = decode_token(token)
    user = user_dict(u_id)
    if user is None:
        return False
    if token in user['tokens']:
        return True
    else:
        return False

# Return a dictionary with the user's authentication data
def user_dict(u_id):
    data = get_data()
    for user in data['users']:
        if u_id == user['u_id']:
            return user
    return None

# Return a dictionary with the channel's data
def channel_dict(channel_id):
    data = get_data()
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return channel
    return None

# Return a dictionary with the message's data
def message_dict(message_id):
    data = get_data()
    for messages in data['messages']:
        if message_id == messages['message_id']:
            return messages
    return None
    
def react_dict(messagedict, react_id):
    data = get_data()
    for react_dict in messagedict['reacts']:
        if react_dict['react_id'] == react_id:
            return react_dict
    return None
    
# Inserts a message into the global message list and channel specific message list
def message_insert(channel_id, message_dict):
    data = get_data()
    channel = channel_dict(channel_id)
    channel['messages'].insert(0, message_dict)
    data['messages'].append(message_dict)
    return

#Removing message from the channel specific message dict
def remove_channel_message_dict(message_id):
    data = get_data()
    channels = data['channels']
    #Obtain the channeldict
    for channeldict in channels:
        #Searches every channeldicts in channel list
        messagelist = channeldict['messages']
        #Searches every messagedict in the messagelist of the channeldict
        for messagedict in messagelist:
            #Find a matching message_id and removes the messagedict from the message list
            if messagedict['message_id'] == message_id:
                messagelist.remove(messagedict)
    return None

# Returns true if the channel has been created already, false if no channel exists
def is_valid_channel(channel_id):
    data = get_data()
    channel_list = data['channels']
    for channels_dict in channel_list:
        if channels_dict['channel_id'] == channel_id:
            return True
    return False

# Returns true if the message has been created already, false if no message exists
def is_valid_message(message_id):
    data = get_data()
    message_list = data['messages']
    for messages_dict in message_list:
        if messages_dict['message_id'] == int(message_id):
            return True
    return False

# Returns True if the user is an owner in the given channel ID, false otherwise
def is_owner(u_id, channel_id):
    channel = channel_dict(channel_id)
    # loop through channel to check if owner
    for dictionary in channel['owner_members']:
        if u_id == dictionary['u_id']:
            return True
    return False

# Returns True if the user is a member in the given channel ID, false otherwise
def is_member(u_id, channel_id):
    channel = channel_dict(channel_id)
    if channel is None:
        return False
    # loop through channel to check if member
    for dictionary in channel['all_members']:
        if u_id == dictionary['u_id']:
            return True
    return False

# Returns a dictionary with the user's first and last name
def get_user_name(u_id):
    data = get_data()
    for user in data['users']:
        if u_id == user['u_id']:
            return {user['name_first'], user['name_last']}
    return None

# Returns a string of the user's first name
def get_first_name(u_id):
    data = get_data()
    user = user_dict(u_id)
    for user in data['users']:
        if u_id == user['u_id']:
            return user['name_first']
    return None

# Returns a string of the user's last name
def get_last_name(u_id):
    data = get_data()
    for user in data['users']:
        if u_id == user['u_id']:
            return user['name_last']
    return None

# Returns a user's ID from their given email
def get_u_id(email):
    data = get_data()
    for user in data['users']:
        if email == user['email']:
            return user['u_id']
    return None

# Returns the user's permission ID - 1: Owner, 2: Admin, 3: Member
def get_permission_id(u_id):
    user = user_dict(u_id)
    return user['permission_id']

# Returns the user's reset code sent after using the password reset feature
def get_reset_code(u_id):
    user = user_dict(u_id)
    return user['reset_code']

# Returns true if email is not being used, false elsewise
def is_email_free(email):
    data = get_data()
    for user in data['users']:
        if user['email'] == email:
            return False
    return True

# Formats a message to be sent via standups
def format_message(u_id, message):
    full_message = ""
    full_message += str(get_first_name(u_id))
    full_message += ": "
    full_message += str(message)
    full_message += "\n"
    return full_message

# Add all the messages into a singe message and send
def standup_string_messages(channel_id):
    new_message = ""
    channel_handler = channel_dict(channel_id)
    for message_summary in channel_handler['standup_queue']:
        new_message += message_summary
    return new_message
###################     PYTEST HELPER FUNCTIONS     ###################

# Clears all data from the database
def reset_data():
    global DATA
    reset_users()
    reset_channels()
    reset_messages()

# Clears all users from the database
def reset_users():
    global DATA
    users = DATA['users']
    users.clear()

# Clears all channels from the database
def reset_channels():
    global DATA
    channels = DATA['channels']
    channels.clear()

# Clears all messages from the database
def reset_messages():
    global DATA
    messages = DATA['messages']
    messages.clear()
    channels = DATA['channels']
    for channeldict in channels:
        messagelist = channeldict['messages']
        messagelist.clear()
