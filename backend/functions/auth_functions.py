from .data import get_data, valid_email, hash_password, get_u_id, user_dict, generate_token, decode_token,is_logged_in
from .exceptions import ValueError, AccessError

def auth_register(email, password, name_first, name_last):

    data = get_data()

    #check if email already exist
    if valid_email(email):
        if get_u_id(email) != None:
            raise ValueError(f"Email: {email} is already registered")
    else:
        raise ValueError(f"Email: {email} is invalid")

    #rules for length of pasword
    MIN_LENGTH = 6
    if len(password) < MIN_LENGTH: 
        raise ValueError(f"Password Length is too short")

    #check first and last name is valid in accordance to specs
    name_check(name_first, name_last)

    #create a unique handle
    handle = ''.join((name_first, name_last))
    generate_handle(handle)

    #prepare u_id, token and password (hashed in db)
    hashedPassword = hash_password(password)
    u_id = 101 + len(data['users'])
    token = generate_token(u_id)

    #generate appropriate permission id
    permission_id = generate_permission_id()

    #append all relevant information to users dictionary
    data['users'].append({
        'email' : email,
        'password' : hashedPassword,
        'name_first' : name_first,
        'name_last' : name_last,
        'u_id': u_id,
        'permission_id' : permission_id,
        'handle' : handle,
        'tokens'  : [token],
        'reset_code' : None,
        'profile_img_url' : None
    })
    #auth_login(email, password)
    return {
        'u_id': u_id,
        'token' : token
    }

def auth_login(email, password):

    data = get_data()
    if not valid_email(email): #check valid email
        raise ValueError(f"Email: {email} is invalid")

    #check if email exists and if so check if password matches
    for user in data['users']:
        if user['email'] == email and user['password'] == hash_password(password):
            u_id = user['u_id']
            token = generate_token(u_id)
            user['tokens'].append(token)
            return {
                'u_id' : u_id,
                'token': token
            }

    raise ValueError(f"Email: {email} does not exist or password is incorrect")

def auth_logout(token):
    if is_logged_in(token): #only logout if user is already logged in
        u_id = decode_token(token)
        user = user_dict(u_id)
        user['tokens'].remove(token)
        return {'is_success' : True}
    else:
        return {'is_success' : False}


def auth_passwordreset_reset(reset_code, new_password):
    data = get_data()
    if len(new_password) < 6:
        raise ValueError("New password is too short")
    for user in data['users']:
        if user['reset_code'] == reset_code and reset_code != None:
            user['reset_code'] = None
            user['password'] = new_password
            return {}
    raise ValueError(f"User does not exist")

######################  HELPER FUNCTIONS  ########################

def name_check(name_first, name_last):
    MAX = 50
    MIN = 1
    if len(name_first) > MAX:
        raise ValueError(f"First name: {name_first} is longer than 50 characters")
    if len(name_first) < MIN:
        raise ValueError(f"First name: {name_first} cannot be empty")
    if len(name_last) > MAX:
        raise ValueError(f"Last name: {name_last} is longer than 50 characters")
    if len(name_last) < MIN:
        raise ValueError(f"Last name: {name_last} cannot be empty")


def generate_handle(handle):
    data = get_data()
    for user in data['users']: #generate unique handle
        if handle == user['handle']:
            handle += str(1 + len(data['users']))

def generate_permission_id():
    data = get_data()
    if len(data['users']) == 0:
        permission_id = 1
    else:
        permission_id = 3
    return permission_id
