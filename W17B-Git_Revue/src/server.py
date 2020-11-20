'''modules'''
import sys
from json import dumps
from threading import Thread
from time import sleep
from flask import Flask, request
from flask_cors import CORS
from error import InputError, AccessError
from auth import auth_login, auth_logout, auth_register, auth_password_request, auth_password_reset
from user import user_profile,\
    user_profile_setemail,\
    user_profile_sethandle,\
    user_profile_setname,\
    user_profile_uploadphoto
from channel import channel_addowner,\
    channel_details,\
    channel_invite,\
    channel_join,\
    channel_leave,\
    channel_messages,\
    channel_removeowner
from message import message_edit,\
    message_react,\
    message_pin,\
    message_remove,\
    message_send,\
    message_sendlater,\
    message_unpin,\
    message_unreact
from channels import channels_create, channels_list, channels_listall
from other import users_all, search
from standup import standup_active, standup_send, standup_start
from helper import check_token, reset_data, get_data, find_id_in_list, get_user_data, load_data, save_data, get_user_from_token
from hangman import start_game, check_word

def default_handler(err):
    '''a default function'''
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, default_handler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    '''an example function'''
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# auth functions
@APP.route('/auth/login', methods={'POST'})
def login():
    '''Given a registered users' email and password,
    generates a valid token for the user to remain authenticated'''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    if email is None or password is None:
        raise InputError(description='Empty email/password')
    res = auth_login(email, password)
    return dumps(res)

@APP.route('/auth/logout', methods={'POST'})
def logout():
    '''Given an active token, invalidates the taken to log the user out. '''
    payload = request.get_json()
    token = payload['token']
    is_success = auth_logout(token)
    return dumps(is_success)

@APP.route('/auth/register', methods={'POST'})
def register():
    '''Given a user's first and last name, email address, and password,
    create a new account for them and return a new token for authentication in their session.'''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']
    if email is None or password is None or name_first is None or name_last is None:
        raise InputError(description='Input error')
    res = auth_register(email, password, name_first, name_last)
    return dumps(res)

@APP.route('/auth/passwordreset/request', methods={'POST'})
def req():
    '''Given a users email send them an email with a rest code'''
    payload = request.get_json()
    email = payload['email']
    if email is None:
        raise InputError(description='Invalid Email')
    res = auth_password_request(email)
    return dumps(res)

@APP.route('/auth/passwordreset/reset', methods={'POST'})
def reset():
    '''Given a reset code a user can change their password'''
    payload = request.get_json()
    new_password = payload['new_password']
    reset_code = payload['reset_code']
    res = auth_password_reset(reset_code, new_password)
    return dumps(res)

# channel functions
@APP.route('/channel/invite', methods={'POST'})
def invite():
    '''Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately'''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    u_id = int(payload['u_id'])
    if channel_id is None or u_id is None:
        raise InputError(description='Empty channel_id/u_id')
    res = channel_invite(token, channel_id, u_id)
    return dumps(res)

@APP.route('/channel/details', methods={'GET'})
def details():
    '''Given a Channel with ID channel_id that the authorised user is part of,
    provide basic details about the channel'''
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    if channel_id is None:
        raise InputError(description='Empty channel_id')
    res = channel_details(token, channel_id)
    return dumps(res)

@APP.route('/channel/messages', methods={'GET'})
def get_messages():
    '''Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50" exclusive.'''
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    if channel_id is None or start is None:
        raise InputError(description='Input error')
    res = channel_messages(token, channel_id, start)
    return dumps(res)

@APP.route('/channel/leave', methods={"POST"})
def leave():
    '''Given a channel ID, the user removed as a member of this channel'''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    if channel_id is None:
        raise InputError(description='Empty channel_id')
    res = channel_leave(token, channel_id)
    return dumps(res)

@APP.route('/channel/join', methods={'POST'})
def join():
    '''Given a channel_id of a channel that the authorised user can join,
    adds them to that channel'''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    if channel_id is None:
        raise InputError(description='Empty channel_id')
    res = channel_join(token, channel_id)
    return dumps(res)

@APP.route('/channel/addowner', methods={'POST'})
def addowner():
    '''Make user with user id u_id an owner of this channel'''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    u_id = int(payload['u_id'])
    if channel_id is None or u_id is None:
        raise InputError(description='Empty channel_id/u_id')
    res = channel_addowner(token, channel_id, u_id)
    return dumps(res)

@APP.route('/channel/removeowner', methods={'POST'})
def removeowner():
    '''Remove user with user id u_id an owner of this channel'''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    u_id = int(payload['u_id'])
    if channel_id is None or u_id is None:
        raise InputError(description='Empty channel_id/u_id')
    res = channel_removeowner(token, channel_id, u_id)
    return dumps(res)

# channels functions
@APP.route('/channels/list', methods={'GET'})
def channelslist():
    '''Provide a list of all channels (and their associated details)
    that the authorised user is part of'''
    token = str(request.args.get('token'))
    channels = channels_list(token)
    return dumps(channels)

@APP.route('/channels/listall', methods={'GET'})
def channelslistall():
    '''Provide a list of all channels (and their associated details)'''
    token = str(request.args.get('token'))
    channels = channels_listall(token)
    return dumps(channels)

@APP.route('/channels/create', methods={'POST'})
def channelscreate():
    '''Creates a new channel with that name that is either a public or private channel'''
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']
    if name is None or is_public is None:
        raise InputError(description='Wrong input')
    channel_id = channels_create(token, name, is_public)
    return dumps(channel_id)

# message functions
@APP.route('/message/send', methods={'POST'})
def msg_send():
    '''Send a message from authorised_user to the channel specified by channel_id'''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    if channel_id is None:
        raise InputError(description='Empty channel id')
    if message is None:
        raise InputError(description='Cannot send empty message')
    data = get_data()
    if message == '/hangman':
        message = start_game(token, channel_id)
        token = data['users'][0]['token']
    if message.split()[0] == '/guess':
        if message == '/guess':
            raise InputError(description='You must enter a letter or a word to guess.')
        guess = message.split()[1]
        message = check_word(token, guess, channel_id)
        token = data['users'][0]['token']
    message_id = message_send(token, channel_id, message)
    return dumps(message_id)

@APP.route('/message/sendlater', methods={'POST'})
def msg_sendlater():
    '''Send a message from authorised_user to the channel specified by
    channel_id automatically at a specified time in the future'''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    time_sent = int(payload['time_sent'])
    if channel_id is None or time_sent is None:
        raise InputError(description='Empty channel id/time sent')
    if message is None:
        raise InputError(description='Cannot send empty message')
    message_id = message_sendlater(token, channel_id, message, time_sent)
    return dumps(message_id)

@APP.route('/message/react', methods={'POST'})
def msg_react():
    '''Given a message within a channel the authorised user is part of,
    add a "react" to that particular message'''
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    react_id = int(payload['react_id'])
    res = message_react(token, message_id, react_id)
    return dumps(res)

@APP.route('/message/unreact', methods={'POST'})
def msg_unreact():
    '''Given a message within a channel the authorised user is part of,
    remove a "react" to that particular message'''
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    react_id = int(payload['react_id'])
    res = message_unreact(token, message_id, react_id)
    return dumps(res)

@APP.route('/message/pin', methods={'POST'})
def pin():
    '''Given a message within a channel, mark it as "pinned" to be given
    special display treatment by the frontend'''
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    res = message_pin(token, message_id)
    return dumps(res)

@APP.route('/message/unpin', methods={'POST'})
def unpin():
    '''Given a message within a channel, remove it's mark as unpinned'''
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    res = message_unpin(token, message_id)
    return dumps(res)

@APP.route('/message/remove', methods={'DELETE'})
def msg_remove():
    '''Given a message_id for a message, this message is removed from the channel'''
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    res = message_remove(token, message_id)
    return dumps(res)

@APP.route('/message/edit', methods={'PUT'})
def msg_edit():
    '''Given a message, update it's text with new text.
    If the new message is an empty string, the message is deleted'''
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    message = payload['message']
    res = message_edit(token, message_id, message)
    return dumps(res)

# user functions
@APP.route('/user/profile', methods={'GET'})
def get_profile():
    '''For a valid user, returns information about their user id,
    email, first name, last name, and handle'''
    token = str(request.args.get('token'))
    u_id = int(request.args.get('u_id'))
    res = user_profile(token, u_id)
    return dumps(res)

@APP.route('/user/profile/setname', methods={'PUT'})
def profile_setname():
    '''Update the authorised user's first and last name'''
    payload = request.get_json()
    token = payload['token']
    first = payload['name_first']
    last = payload['name_last']
    res = user_profile_setname(token, first, last)
    return dumps(res)

@APP.route('/user/profile/setemail', methods={'PUT'})
def profile_setemail():
    '''Update the authorised user's email address'''
    payload = request.get_json()
    token = payload['token']
    email = payload['email']
    res = user_profile_setemail(token, email)
    return dumps(res)

@APP.route('/user/profile/sethandle', methods={'PUT'})
def profile_sethandle():
    '''Update the authorised user's handle (i.e. display name)'''
    payload = request.get_json()
    token = payload['token']
    handle = payload['handle_str']
    res = user_profile_sethandle(token, handle)
    return dumps(res)

@APP.route('/user/profile/uploadphoto', methods={'POST'})
def uploadphoto():
    '''Given an image url the image is cropped and set as a profile picture'''
    payload = request.get_json()
    token = payload['token']
    img_url = payload['img_url']
    x_start = int(payload['x_start'])
    y_start = int(payload['y_start'])
    x_end = int(payload['x_end'])
    y_end = int(payload['y_end'])
    res = user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)
    return dumps(res)

# other functions
@APP.route('/users/all', methods={'GET'})
def show_all():
    '''Returns a list of all users and their associated details'''
    return dumps(users_all(request.args.get('token')))

@APP.route('/search', methods={'GET'})
def run_search():
    '''Given a query string, return a collection of messages in all of
    the channels that the user has joined that match the query.
    Results are sorted from most recent message to least recent message'''
    return dumps(search(request.args.get('token'), request.args.get('query_str')))

@APP.route('/standup/start', methods={'POST'})
def standupstart():
    '''Starts a standup'''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    length = int(payload['length'])
    if length is None:
        raise InputError(description='No length specified')
    time_finish = standup_start(token, channel_id, length)
    return dumps(time_finish)

@APP.route('/standup/active', methods={'GET'})
def standupactive():
    '''Check if the standup is active and when it ends'''
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    is_active = standup_active(token, channel_id)
    return dumps(is_active)

@APP.route('/standup/send', methods={'POST'})
def standupsend():
    '''Send a message to the standup'''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    if message is None:
        raise InputError(description='Empty message')
    res = standup_send(token, channel_id, message)
    return dumps(res)

@APP.route('/admin/userpermission/change', methods={'POST'})
def userpermission_change():
    '''admian change user's permission id'''
    data = get_data()
    payload = request.get_json()
    token = payload['token']
    check_token(token)
    u_id = int(payload['u_id'])
    permission_id = int(payload['permission_id'])
    if u_id is None or permission_id is None:
        raise InputError(description='Empty input')
    if permission_id != 1 and permission_id != 2:
        raise InputError(description='Invalid permission id')
    if get_user_data(u_id) == {}:
        raise InputError(description='No such user exists')
    for user in data['users']:
        if user['u_id'] == u_id:
            user['permission_id'] = permission_id
    return dumps({})

@APP.route('/admin/user/remove', methods={'DELETE'})
def user_remove():
    '''admin removes a user from slackr'''
    data = get_data()
    payload = request.get_json()
    token = payload['token']
    u_id = int(payload['u_id'])
    check_token(token)

    user_data = get_user_data(u_id)
    if user_data == {}:
        raise InputError(description='No such user exists')
    person_u_id = get_user_from_token(token)
    person_data = get_user_data(person_u_id)
    if person_data['permission_id'] != 1:
        raise AccessError(description='The authorised person is not an owner of slackr')
    user_info = {
        'u_id': u_id,
        'name_first': user_data['name_first'],
        'name_last': user_data['name_last'],
    }
    for channel in data['channels']:
        if user_info in channel['owner_members']:
            curr_channel_id = channel['channel_id']
            data['channels'][curr_channel_id - 1]['owner_members'].remove(user_info)
            data['channels'][curr_channel_id - 1]['all_members'].remove(user_info)
        elif user_info in channel['all_members']:
            curr_channel_id = channel['channel_id']
            data['channels'][curr_channel_id - 1]['all_members'].remove(user_info)
    dumps({})

@APP.route('/workspace/reset', methods={'POST'})
def workspace_reset():
    '''Resets the workspace state'''
    reset_data()
    return dumps({})

def persistence():
    '''Persists data every 10 seconds'''
    while True:
        save_data()
        sleep(10)

if __name__ == "__main__":
    load_data()
    SAVE = Thread(target=persistence, daemon=True)
    SAVE.start()
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8084))
