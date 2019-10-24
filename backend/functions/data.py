from json import dumps
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
import hashlib
import jwt
import re
import copy
import time
from .exceptions import *
#GLOBAL VARIABLES
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
SECRET = "daenerys"
data = {
    'users' : [], # should have a dictionary for each user
    'channels' : [], #shoudl have a dictionary for each channel
    'messages' : [] #should have a dictionary for each messages
    # e.g. {email, password, name_first, name_last, u_id, permission_id, handle, token, profile, is_logged}

    #e.g {channel_id, 'name' : channelname, 'owners' : ['u_id': u_id1, u_id2...], members : [u_id, u_id2....], 'is_public': True , messages = []}
}

#check if email is valid
def valid_email(email):
    if(re.search(regex,email)):
        return True
    else:
        return False

#abstraction for returning global data
def get_data():
    global data
    return data

#abstraction for returning json string
def send(data):
    return dumps(data)


#encodes token given string and SECRET
def generate_token(string):
    global SECRET
    return jwt.encode({'string' : string, 'time' : time.time()}, SECRET, algorithm='HS256').decode('utf-8')

#decodes token given string and SECRET
def decode_token(token):
    global SECRET
    decoded = jwt.decode(token.encode('utf-8'), SECRET, algorithms=['HS256'])
    return decoded['string']

#generates hash for string
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_logged_in(token):

    u_id = decode_token(token)
    user = user_dict(u_id)
    if user == None:
        return False
    if token in user['tokens']:
        return True
    else:
        return False

def user_dict(u_id):
    data = get_data()
    for user in data['users']:
        if u_id == user['u_id']:
            return user
    return None

def channel_dict(channel_id):
    data = get_data()
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return channel
    return None

def message_dict(message_id):
    data = get_data()
    for messages in data['messages']:
        if message_id == messages['message_id']:
            return messages
    return None

def is_joined(token, channel_id):
    data = get_data()
    u_id = decode_token(token)
    for channel_dict in data['channels']:
        if u_id in channel_dict['all_members']:
            return True
    return False

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

def is_owner(u_id, channel_id):
    channel = channel_dict(channel_id)
    # loop through channel to check if owner
    for dict in channel['owner_members']:
        if u_id == dict['u_id']:
            return True
    return False

def is_member(u_id, channel_id):
    channel = channel_dict(channel_id)
    # loop through channel to check if member
    for dict in channel['all_members']:
        if u_id == dict['u_id']:
            return True
    return False

def get_first_name(u_id):
    user = user_dict(u_id)
    for user in data['users']:
        if u_id == user['u_id']:
            return user['name_first']
    return None

def get_last_name(u_id):
    data = get_data()
    for user in data['users']:
        if u_id == user['u_id']:
            return user['name_last']
    return None
