"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request
import hashlib
import jwt
import re
import copy
import time

from backend.functions.data import *
from backend.functions.auth_functions import *
from backend.functions.channel_functions import *
from backend.functions.message_functions import *

APP = Flask(__name__)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)

#########################   AUTH FUNCTIONS  ###########################

#REGISTER
@APP.route('/auth/register', methods = ['POST'])
def create():

    email = request.form.get('email') #get email
    password = request.form.get('password') # get password
    name_first = request.form.get('name_first') #get first name
    name_last = request.form.get('name_last') #get last name

    return send(auth_register(email, password, name_first, name_last));

#LOGIN
@APP.route('/auth/login', methods = ['PUT'])
def connect():

    email = request.form.get('email') #get email
    password = request.form.get('password') #get password


    return send(auth_login(email, password))


#INVITE
@APP.route('/channel/invite', methods = ['POST'])
def invite():

    token = request.form.get('token') #get token
    channel_id = request.form.get('channel_id') #get channel_id
    u_id = request.form.get('u_id') #get u_id


    return send(channel_invite(token, channel_id, u_id))



#JOIN
@APP.route('/channel/join', methods = ['POST'])
def join():

    token = request.form.get('token') #get token
    channel_id = int(request.form.get('channel_id')) #get channel_id


    return send(channel_join(token, channel_id))

@APP.route('/auth/logout', methods = ['PUT'])
def logout():

    token = request.form.get('token') #get token


    return send(auth_logout(token))

#########################   CHANNEL FUNCTIONS  ###########################

@APP.route('/channels/create', methods = ['POST'])
def channel_create():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')

    return send(channels_create(token, name, is_public))


@APP.route('/channels/listall', methods = ['GET'])
def listall():
    token = request.args.get('token')
    return send(channels_listall(token))


@APP.route('/channels/list', methods = ['GET'])
def list():
    token = request.args.get('token')
    return send(channels_list(token))

@APP.route('/channel/leave', methods = ['POST'])
def leave():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))

    return send(channel_leave(token, channel_id))

@APP.route('/channel/addowner', methods = ['POST'])
def addowner():
    token = request.form.get('token')   # person doing promoting
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))     # person being promoted

    return send(channel_addowner(token, channel_id, u_id))

@APP.route('/channel/removeowner', methods = ['POST'])
def removeowner():
    token = request.form.get('token')   # person doing demoting
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))     # person being demoted

    return send(channel_removeowner(token, channel_id, u_id))

@APP.route('/channel/messages', methods = ['GET'])
def listmessages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id')) #must be valid channel
    start = int(request.args.get('start')) #cannot be >= no. of messages in channel

    return dumps(channel_messages(token, channel_id, start), indent=4, sort_keys=True, default=str)

@APP.route('/channel/details', methods = ['GET'])
def details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    return send(channel_details(token, channel_id))

#########################   MESSAGE FUNCTIONS  ###########################

@APP.route('/message/send', methods = ['POST'])
def sendmessages():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')

    return send(message_send(token, channel_id, message))

@APP.route('/message/edit', methods = ['PUT'])
def editmessages():
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    message = request.form.get('message')

    return send(message_edit(token, message_id, message))

@APP.route('/message/react', methods = ['POST'])
def reactmessages():
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    react_id = request.form.get('react_id')

    return send(message_react(token, message_id, react_id))

@APP.route('/message/unreact', methods = ['POST'])
def unreactmessages():
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    react_id = request.form.get('react_id')

    return send(message_unreact(token, message_id, react_id))

@APP.route('/message/pin', methods = ['POST'])
def pinmessages():
    token = request.form.get('token')
    message_id = request.form.get('message_id')

    return send(message_pin(token, message_id))

@APP.route('/message/unpin', methods = ['POST'])
def unpinmessages():
    token = request.form.get('token')
    message_id = request.form.get('message_id')

    return send(message_unpin(token, message_id))

if __name__ == "__main__":
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000), debug=True)
