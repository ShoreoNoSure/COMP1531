'''A bank of helper functions that can be imported'''
# pylint: disable = anomalous-backslash-in-string, global-statement, global-at-module-level, line-too-long
from shutil import rmtree
import os
import re
from json import load, dump
import hashlib
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jwt
from error import AccessError

SECRET = 'shrek2'

global DATA
DATA = {}

# Make a regular expression validating an Email
REGEX = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def check(email):
    '''Checks that the email is valid'''
    # pass the regualar expression and the string in search() method
    if re.search(REGEX, email):
        return True
    return False

def reset_data():
    '''
    Resets the global data

    Parameters:

    Returns:
        A Dictionary with an empty set of the global data

    Errors:
    '''
    global DATA
    DATA = {
        'users': [{
            'u_id': 0,
            'name_first': 'hangman',
            'name_last': 'bot',
            'password': '000000',
            'email': 'z1234567@unsw.edu.au',
            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjowfQ.n0yIyUboqdoiEsO0Up-J2vdUe619Nw8PzFahPGe7jvw',
            'reset_code': 0,
            'logged_in': 0,
            'handle_str': 'hangmanbot',
            'permission_id': 2,
            'profile_img_url': '',
        }],
        'channels': [],
        'messages': [],
        'hangman': [],
        'standup': {
            'u_id': 0,
            'channel_id': 0,
            'time_finish': 0,
            'message': '',
            'buffer': []
        }
    }
    if os.path.exists('static'):
        rmtree('static')
    return DATA

def get_data():
    '''
    Retrieves global data

    Parameters:

    Returns:
        A Dictionary with the stored global data

    Errors:
    '''
    global DATA
    return DATA

def save_data():
    '''
    Stores the data in a json file

    Parameters:

    Returns:
        An empty dictionary

    Errors:
    '''
    global DATA
    with open('export.json', 'w') as filepath:
        dump(DATA, filepath)
    return {}

def load_data():
    '''
    Loads the stored data we already have saved

    Parameters:

    Returns:
        An empty dictionary

    Errors:
    '''
    global DATA
    with open('export.json', 'r') as filepath:
        DATA = load(filepath)
    return {}

def get_user_data(u_id):
    '''
    Return user's information dict from data

    Parameters:
        u_id - The user id number to be returning the data for

    Returns:
        A dictionary containing the user's information

    Errors:
    '''
    user_data = {}
    data = get_data()
    for user in data['users']:
        if user['u_id'] == u_id:
            return user
    return {}

def send_success(data):
    '''Returns success'''
    return dumps(data)

def send_error(message):
    '''Sends an error message'''
    return dumps({
        '_error' : message,
    })

def generate_token(u_id):
    '''
    Generates a token from the u_id

    Parameters:
        u_id - The user id number to be generating a token for

    Returns:
        An endcoded string to be used as the users token

    Errors:
    '''
    global SECRET
    encoded = jwt.encode({'u_id': u_id}, SECRET, 'HS256').decode('utf-8')
    return str(encoded)

def get_user_from_token(token):
    '''
    Decodes token and gives back a u_id

    Parameters:
        token - The user's token that was generated from their user id

    Returns:
        The user's u_id

    Errors:
    '''
    check_token(token)
    global SECRET
    decoded = jwt.decode(token, SECRET, algorithms=['HS256'])
    return int(decoded['u_id'])

def check_token(token):
    '''
    Checks if token is valid
    Parameters:
        token - The user's token that was generated from their user id

    Returns:

    Errors:
        AccessError:
            The token is invalid
    '''
    data = get_data()
    for user in data['users']:
        if (token == user['token'] and user['logged_in'] == 1) or user['u_id'] == 0:
            return
    raise AccessError(description='token is invalid')

def hash_password(password):
    '''
    Encodes password

    Parameters:
        password - The password to be encoded

    Returns:
        An encoded password
    Errors:
    '''
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def get_handle(first_name, last_name):
    '''
    Generates the handle for a user by concatenating their first and last name.
    Measures in place to stop repeated handles

    Parameters:
        first_name - The users first name
        last_name - The users last name

    Returns:
        A handle for the user
    Errors:
    '''
    handle = first_name.lower() + last_name.lower()
    if len(handle) > 18:
        handle = handle[:18]
    while is_handle_unique(handle) == 0:
        if len(handle) >= 20:
            handle = handle[:19]
        handle = handle + str(random.randint(0, 9))
    return handle

def is_handle_unique(handle):
    '''
    Goes through all handles to check if a given handle is unique

    Parameters:
        first_name - The users first name
        last_name - The users last name

    Returns:
        A 1 if the handle is unique
        A 0 if the handle is not unique

    Errors:
    '''
    data = get_data()
    i = 0
    while i < len(data['users']):
        if data['users'][i]['handle_str'] == handle:
            return 0
        i += 1
    return 1

def find_id_in_list(data_list, data_id, data_id_type):
    '''
    Returns whether or not the id given exists within the list
    Parameters:
        data_list - The list of data we are searching through
        data_id - The id we are searching for
        data_id_type - The type of id we are searching for

    Returns:
        True if the data_id is found in the list
        False if the data_id is not found in the list
    Errors:
    '''
    for element in data_list:
        if element[data_id_type] == data_id:
            return True
    return False

def send_standup_package():
    '''Adds the standup package to the list of messages

    Parameters:

    Returns:
        An empty dictionary

    Errors:
    '''
    data = get_data()
    standup = data['standup']
    if standup['message'] == '':
        return {}
    new_message = {
        'u_id': standup['u_id'],
        'channel_id': standup['channel_id'],
        'message_id': len(data['messages']) + 1,
        'message': standup['message'],
        'time_created': standup['time_finish'],
        'send_later': False,
        'react': [],
        'is_pinned': 0,
    }
    # Insert at start of list
    data['messages'].insert(0, new_message)
    standup['message'] = ''
    standup['buffer'] = []
    return {}

def generate_reset_code():
    '''generate reset code'''
    reset_code = ""
    for _ in range(10):
        reset_code = reset_code + str(random.randint(0, 9))
    return reset_code

def send_email(email, reset_code):
    '''Send an email'''
    email_content = 'This email was sent in order to reset your password. \
        If you have not requested a pssword reset please ignore this email. \
        Someone may be trying to hack into your account and \
        it is recommended you change your password, the code is ' + str(reset_code) + '.'

    #The mail addresses and password
    sender_address = 'GitRevueSlackr@gmail.com'
    sender_pass = 'AnimalCrossing'
    receiver_address = str(email)
    #Setup Mime
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Password Reset'
    #The body and the attachments for the mail
    message.attach(MIMEText(email_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP(host='smtp.gmail.com', port=587) #use gmail with port
    session.starttls() #Security
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

def get_max_msg_id():
    ''' get the maximum message id based on DATA

    Parameters:

    Returns:
        The maximum number message_id

    Errors:
    '''
    data = get_data()
    maximum = 0
    for msg in data['messages']:
        if msg['message_id'] > maximum:
            maximum = msg['message_id']
    return maximum

def get_max_u_id():
    '''
    get the maximum user id

    Parameters:

    Returns:
        The maximum number user_id

    Errors:
    '''
    data = get_data()
    maximum = 0
    for user in data['users']:
        if user['u_id'] > maximum:
            maximum = user['u_id']
    return maximum
