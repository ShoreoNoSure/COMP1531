'''This program contains authentication functions according to the spec'''
from error import InputError
from helper import get_data, get_user_from_token, generate_token, \
    hash_password, get_handle, check, check_token, get_max_u_id, \
    send_email, generate_reset_code

def auth_login(email, password):
    '''This program logs a user in'''
    data = get_data()
    # Check email
    if check(email) is False:
        raise InputError(description="Invalid Email")
    #Password check
    password = hash_password(password)
    for user in data['users']:
        #if found a matching email
        if user['email'] == email:
            if user['password'] != password:
                #Not correct password
                raise InputError(description="Incorrect Password")
            else:
                #if password correct
                u_id = user['u_id']
                user['logged_in'] = 1
                #generate a token
                token = generate_token(u_id)
                return {'u_id':u_id, 'token': token}
    # No matching email
    raise InputError(description="No user found with this email")

def auth_logout(token):
    '''This program logs a user out'''
    check_token(token)
    data = get_data()
    u_id = get_user_from_token(token)
    for user in data['users']:
        if user['u_id'] == u_id:
            # Set the specified users login flag to 0 to log them off
            if user['logged_in'] == 1:
                user['logged_in'] = 0
                return {'is_success' : True}
    return {'is_success' : False}

def auth_register(email, password, name_first, name_last):
    '''This program registers a user'''
    data = get_data()
    # check email
    if check(email) is False:
        raise InputError(description="Invalid Email")
    # Invalid password
    if len(password) < 6:
        raise InputError(description="Invalid Password")
    # Invalid firstname
    if not name_first or len(name_first) > 50:
        raise InputError(description="Invalid First Name")
    # Invalid Lastname
    if not name_last or len(name_last) > 50:
        raise InputError(description="Invalid Last Name")
    # Email already in use
    for user in data['users']:
        if user['email'] == email:
            raise InputError(description="Email already in use")

    # New user for backend
    u_id = get_max_u_id() + 1
    # Assume that you are logged in once you register
    token = generate_token(u_id)
    new_user = {
        'u_id': u_id,
        'name_first': name_first,
        'name_last': name_last,
        'password': str(hash_password(password)),
        'email': email,
        'token': token,
        'reset_code': 0,
        'logged_in': 1,
        'handle_str': get_handle(name_first, name_last),
        'permission_id': 2,
        'profile_img_url': ''
    }
    data['users'].append(new_user)
    # Owner permision id = 1 normal memeber id = 2
    if u_id == 1:
        new_user['permission_id'] = 1
    return {"u_id": u_id, "token": token}
    
def auth_password_reset(reset_code, new_password):
    '''This program resets a users password given a reset code'''
    data = get_data()
    if len(new_password) < 6:
        raise InputError("Invalid password, must be longer")
    for user in data['users']:
        # Check if the reset code given was an currently active for a user
        if user['reset_code'] == reset_code:
            user['password'] = str(hash_password(new_password))
            return {}
    raise InputError("Reset code incorrect")

def auth_password_request(email):
    '''This program requests a password change and sends the user a reset code'''
    data = get_data()
    valid_email = -1
    for user in data['users']:
        if user['email'] == email:
            valid_email = 1
            break
    if valid_email == -1:
        raise InputError("Invalid Email")
    #Create a temporary field for this user called reset_code
    #When entered correctly it will be reset
    user['reset_code'] = generate_reset_code()
    # Format of this message is important for else the subject field won't
    # actually be the email subject.
    send_email(email, str(user['reset_code']))
    return {}