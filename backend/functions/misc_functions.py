from .data import *
from datetime import datetime, timedelta, timezone

# Returns messages featuring the 'query_str' keyword from
# channels that the user is part of
def search(token, query_str):
	data = get_data()
	messages = []
	for message_dict in data['messages']:
		if query_str in message_dict['message']:
			messages.append(message_dict)

	return {'messages': messages}


def admin_userpermission_change(token, u_id, permission_id):
	if permission_id != 1 and permission_id != 2 and permission_id != 3:
		raise ValueError(f"Invalid permission id change: {permission_id} requested")

	caller_id = decode_token(token)
	caller_user = user_dict(caller_id)
	secondary_user = user_dict(u_id)
	if secondary_user == None:
		raise ValueError(f"User ID: {u_id} does not refer to a valid user")

	caller_permission = caller_user['permission_id']
	if caller_permission == 3:
		raise AccessError(f"Authorised user: {caller_id} is not an admin or owner")

	if caller_permission == 1 or secondary_user['permission_id'] != 1:
		secondary_user['permission_id'] = permission_id
	else:
		raise AccessError("Owner cannot change admin permissions")

	return {}

def standup_start(token, channel_id, length):

	data = get_data()

	if channel_dict(channel_id) is None:
		raise ValueError(f"Channel ID: {channel_id} does not exist")
	if is_member(decode_token(token), channel_id) is False:
		raise AccessError(f"Authorised User: {decode_token(token)} is not a member of the channel")

	channelHandler = channel_dict(channel_id)

	if channelHandler['standup_active'] is False:
		channelHandler['standup_active'] = True
		EndTime = datetime.now() + timedelta(seconds=length)
		EndTimeStr = EndTime.strftime("%H:%M:%S")
		print("The standup has begun, and will stop at: ")
		print(EndTimeStr)
		timestamp = EndTime.replace().timestamp()
		channelHandler['standup_end'] = timestamp
		return {'time_finish': timestamp}
	else:
		raise ValueError(f"Standup already running on this channel ID: {channel_id}")



def standup_send(token, channel_id, message):

	data = get_data()

	channelHandler = channel_dict(channel_id)

	if channel_dict(channel_id) is None:
		raise ValueError(f"Channel ID: {channel_id} does not exist")
	if len(message) > 1000:
		raise ValueError ("Message is more than 1000 characters long")
	if len(message) < 1:
		raise ValueError ("Message cannot be empty")
	if is_member(decode_token(token) ,channel_id) is False:
		raise AccessError(f"Authorised User: {decode_token(token)} is not a member of the channel")
	if channelHandler['standup_active'] is False:
		raise ValueError (f"There is no standup running in channel ID: {channel_id}")

	channelHandler['standup_queue'].append(message)
	return{}

def standup_active(token, channel_id):
	data = get_data()

	if channel_dict(channel_id) is None:
		raise ValueError(f"Channel ID: {channel_id} does not exist")
	if is_member(decode_token(token), channel_id) is False:
		raise AccessError(f"Authorised User: {decode_token(token)} is not a member of the channel")

	channelHandler = channel_dict(channel_id)

	NowTime = datetime.now()
	NowTimeStr = NowTime.strftime("%H:%M:%S")
	if NowTime < channelHandlerp['standup_end']
	if channelHandler['standup_active'] is False:
		channelHandler['standup_active'] = True
		return {
			'is_active': True,
			'time_finish': channelHandler['standup_end']
		}
	else:
		channelHandler['standup_active'] = False
		return {
			'is_active': False,
			'time_finish': channelHandler['standup_end']
		}
