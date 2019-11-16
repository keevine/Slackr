from .exceptions import ValueError, AccessError
from .data import decode_token, valid_email, is_email_free, user_dict, channel_dict, get_data
import sys
from PIL import Image
import urllib.request



def user_profile_setemail(token, email):
	# Using helper functions, return data
	u_id = decode_token(token)
	userData = user_dict(u_id)
	# Raise errors if the user and email are not valid
	if valid_email(email) is False:
		raise ValueError(f"Email: {email} entered is not a valid email")
	if is_email_free(email) == 0:
		raise ValueError(f"Email: {email} is already in use")
	# At this point, the email is valid and untaken, so replace the old one

	userData['email'] = email
	print("Successfully updated user's email")

	return {}


def user_profile_sethandle(token, handle_str):
	# Using helper functions, return data
	u_id = decode_token(token)
	userData = user_dict(u_id)
	# Raise errors if the user and handle are not valid
	if len(handle_str) > 20:
		raise ValueError(f"Handle: {handle_str} is larger than 20 characters")
	if len(handle_str) < 1:
		raise ValueError("Handle cannot be empty")
	# At this point, the handle is valid, so replace the old one
	userData['handle'] = handle_str
	print("Successfully updated user's handle")

	return {}

def user_profile_setname(token, name_first, name_last):
	# Using helper functions, return data
	u_id = decode_token(token)
	userData = user_dict(u_id)
	# Raise errors if the user and names are not valid
	if len(name_first) > 50:
		raise ValueError(f"First name: {name_first} is longer than 50 characters")
	if len(name_first) < 1:
		raise ValueError(f"First name: {name_first} cannot be empty")
	if len(name_last) > 50:
		raise ValueError(f"Last name: {name_last} is longer than 50 characters")
	if len(name_last) < 1:
		raise ValueError(f"Last name: {name_last} cannot be empty")
	# At this point, the names are valid, so replace the old one
	userData['name_first'] = name_first
	userData['name_last'] = name_last
	print("Successfully updated user's first and last name")

	return {}

def user_profile(token,u_id):
	# Using helper functions, return data
	userData = user_dict(u_id)
	# Raise errors if the user and names are not valid
	if userData == None:
		raise ValueError(f"User ID: {u_id} does not exist")
	# Return the user dictionary of information
	new_dict = {
        'email': userData['email'],
        'name_first': userData['name_first'],
        'name_last': userData['name_last'],
        'handle_str': userData["handle"]
    }
	# Returns dict containing {email,name_first,name_last,handle_str}
	print("Successfully found and located user's information")
	return new_dict

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
	# Append img_url to user data
	user = user_dict(decode_token(token))
	user['profile_img_url'] = img_url
	# Extract the image from the URL and store at 'filePath' location

	# Create a counter to store unique photos i.e photo1.png, photo2.png etc
	# At the moment this doesnt work because I haven't made it global so it
	# will always be 1
	userCounter = 1
	filePath = "backend/functions/pictures/profile_pic" + str(userCounter) + ".jpg"
	userCounter += 1
	# Save the picture from the URL to the filepath
	urllib.request.urlretrieve(img_url,filePath)
	# Print to debug to terminal
	print("Successfully saved the user image")
	
	# Crop picture section
	# Open the image
	imageObject = Image.open(filePath)
	# Crop to dimensions and save
	cropped = imageObject.crop((x_start, y_start, x_end, y_end))
	cropped.save(filePath)
	# Print to debug to terminal
	print("Successfully cropped the user image")
	# Return nothing as specified
	return{}

def user_listall(token):
	data = get_data()
	user_list = []
	for user_dict in data['users']:
		# Extract the relevant info into a dictionary and append to a list to return
		dict = {
			'u_id': user_dict['u_id'],
			'email': user_dict['email'],
			'name_first': user_dict['name_first'],
			'name_last': user_dict['name_last'],
			'handle_str': user_dict['handle'],
			'profile_img_url': user_dict['profile_img_url']
		}
		user_list.append(dict)

	return {'users': user_list}
