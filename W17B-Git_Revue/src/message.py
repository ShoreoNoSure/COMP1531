'''
message_send - Sends a message
message_sendlater - Sends a message later
message_react - Reacts to a message
message_unreact - Unreacts a message
message_pin - Pins a message
message_unpin - Unpins a message
message_remove - Removes a message
message_edit - Edits a message
'''
from datetime import datetime, timezone
import threading
from error import InputError, AccessError
from helper import get_user_from_token, check_token, find_id_in_list, get_data, get_max_msg_id,\
     get_user_data

def message_send(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id

    Parameters:
        token - The user's token that was generated from their user id
        channel_id - The id the user wishes to message
        message - The message the user wishes to send

    Returns:
        A dictionary containing a message_id

    Errors:
        InputError:
            Message is more than 1000 characters
        AccessError:
           The authorised user has not joined the channel they are trying to post to
    '''
    # Check if user is valid
    check_token(token)
    # Check if message is too long
    if len(message) > 1000:
        raise InputError(description="Message is too long")
    data = get_data()
    u_id = get_user_from_token(token)
    # Find the channel with channel_id
    curr_channel = data['channels'][channel_id - 1]
    # Check if user is in this channel
    if not find_id_in_list(curr_channel['all_members'], u_id, 'u_id') and u_id != 0:
        raise AccessError(description="User is not in channel")
    # Get the time when message is sent
    curr_time = datetime.utcnow()
    timestamp = curr_time.replace(tzinfo=timezone.utc).timestamp()
    # Get message id based on the lastest (max) message id
    message_id = get_max_msg_id() + 1
    new_message = {
        'u_id': u_id,
        'channel_id': channel_id,
        'message_id': message_id,
        'message': message,
        'time_created': timestamp,
        'send_later': False,
        'react': [],
        'is_pinned': False
    }
    # insert new message to the start of list
    data['messages'].insert(0, new_message)
    return {'message_id': message_id}

def message_remove(token, message_id):
    '''
    Given a message_id for a message, this message is removed from the channel

    Parameters:
        token - The user's token that was generated from their user id
        message_id - Id of the message the user wishes to remove

    Returns:
        An empty dictionary

    Errors:
        InputError:
            Message (based on ID) no longer exists
        AccessError when none of the following are true:
            Message with message_id was sent by the authorised user making this request
            The authorised user is an owner of this channel or the slackr
    '''
    check_token(token)
    data = get_data()
    # Check if message exists
    if not find_id_in_list(data['messages'], message_id, 'message_id'):
        raise InputError(description="Message no longer exists")
    u_id = get_user_from_token(token)
    for message in data['messages']:
        if message['message_id'] == message_id:
            channel_id = message['channel_id']
            curr_channel = data['channels'][channel_id - 1]
            user = data['users'][u_id - 1]
            is_owner = find_id_in_list(curr_channel['owner_members'], u_id, 'u_id')
            if message['u_id'] == u_id or is_owner or user['permission_id'] == 1:
                data['messages'].remove(message)
                return {}
    raise AccessError(description="You did not send this message or are not an owner")

def message_sendlater(token, channel_id, message, time_sent):
    '''
    Send a message from authorised_user to the channel \
         specified by channel_id automatically at a specified time in the future

    Parameters:
        token - The user's token that was generated from their user id
        channel_id - The id of the channel the user wishes to message
        message - The message the user wishes to send
        time_sent

    Returns:
        A dictionary containing a bool is_sucess

    Errors:
        InputError:
            Channel ID is not a valid channel
            Message is more than 1000 characters
            Time sent is a time in the past
        AccessError:
            The authorised user has not joined the channel they are trying to post to
    '''
    check_token(token)
    data = get_data()
    #check channel exist
    if not find_id_in_list(data['channels'], channel_id, 'channel_id'):
        raise InputError(description="Channel does not exist")
    if len(message) > 1000:
        raise InputError(description="Message is too long")
    curr_time = datetime.utcnow()
    time_stamp = int(time.mktime(curr_time.timetuple()))
    if time_sent < time_stamp:
        raise InputError(description="Cannot send messages in the past")
    curr_channel = data['channels'][int(channel_id) - 1]
    u_id = get_user_from_token(token)
    if not find_id_in_list(curr_channel['all_members'], u_id, 'u_id'):
        raise AccessError("Cannot send messages in channels you're not in")
    message_id = get_max_msg_id() + 1
    new_message = {
        'u_id': u_id,
        'channel_id': channel_id,
        'message_id': message_id,
        'message': message,
        'time_created': time_sent,
        'send_later': True,
        'react': [],
        'is_pinned': False
    }
    curr_time = datetime.utcnow()
    time_stamp = int(time.mktime(curr_time.timetuple()))
    timer = threading.Timer(time_sent - time_stamp, data['messages'].insert(0, new_message))
    timer.start()
    return {"message_id" : new_message['message_id']}

def message_pin(token, message_id):
    '''
    Given a message within a channel, mark it as "pinned" to be given special display treatment\
         by the frontend

    Parameters:
        token - The user's token that was generated from their user id
        message_id - The message id which the user wishes to pin

    Returns:
        An empty dictionary

    Errors:
        InputError:
            Message_id is not a valid message
            Message with ID message_id is already pinned
        AccessError:
            The authorised user is not a member of the channel that the message is within
            The authorised user is not an owner
    '''
    check_token(token)
    data = get_data()
    if not find_id_in_list(data['messages'], message_id, 'message_id'):
        raise InputError(description="Message does not exist")
    # msg exists
    for message in data['messages']:
        if message['message_id'] == message_id:
            msg = message
    if msg['is_pinned']:
        raise InputError(description="This message is already pinned")
    u_id = get_user_from_token(token)
    user = data['users'][u_id - 1]
    for channel in data['channels']:
        if not find_id_in_list(channel['all_members'], u_id, 'u_id'):
            raise AccessError(description='The authorised user is not in this channel')
        else:
            curr_channel = channel
    if find_id_in_list(curr_channel['owner_members'], u_id, 'u_id') or user['permission_id'] == 1:
        msg['is_pinned'] = True
        return {}
    raise InputError(description="The authorised user does not have owner priveledge \
        to pin message in this channel")

def message_unpin(token, message_id):
    '''
    Given a message within a channel, remove it's mark as unpinned

    Parameters:
        token - The user's token that was generated from their user id
        message_id - The id of the message to be unpinnned

    Returns:
        An empty dictionary

    Errors:
        InputError:
            Message_id is not a valid message
            Message with ID message_id is already unpinned
        AccessError:
            The authorised user is not a member of the channel that the message is within
            The authorised user is not an owner
    '''
    check_token(token)
    data = get_data()
    if not find_id_in_list(data['messages'], message_id, 'message_id'):
        raise InputError(description="Message does not exist")
    for message in data['messages']:
        if message['message_id'] == message_id:
            msg = message
    if not msg['is_pinned']:
        raise InputError(description="This message is not pinned")
    u_id = get_user_from_token(token)
    user = data['users'][u_id - 1]
    for channel in data['channels']:
        if not find_id_in_list(channel['all_members'], u_id, 'u_id'):
            raise AccessError(description='The authorised user is not in this channel')
        else:
            curr_channel = channel
    if find_id_in_list(curr_channel['owner_members'], u_id, 'u_id') or user['permission_id'] == 1:
        msg['is_pinned'] = False
        return {}
    raise InputError(description="The authorised user does not have owner priveledge \
        to unpin message in this channel")

def message_react(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of, add a "react" to \
        that particular message

    Parameters:
        token - The user's token that was generated from their user id
        message_id - The id of the message to be reacted to
        react_id - What type of reaction is shown

    Returns:
        An empty dictionary

    Errors:
        InputError:
            Message_id is not a valid message within a channel that the authorised user has joined
            React_id is not a valid React ID. The only valid react ID the frontend has is 1
            Message with ID message_id already contains an active React with ID react_id \
                from the authorised user
    '''
    check_token(token)
    data = get_data()
    # The only valid react ID the frontend has is 1
    if react_id != 1:
        raise InputError(description="Invalid React ID")
    if not find_id_in_list(data['messages'], message_id, 'message_id'):
        raise InputError(description="Message_id is not a valid message within a \
            channel that the authorised user has joined")
    for message in data['messages']:
        if message['message_id'] == message_id:
            msg = message
    u_id = get_user_from_token(token)
    channel_id = msg['channel_id']
    curr_channel = data['channels'][channel_id - 1]
    if not find_id_in_list(curr_channel['all_members'], u_id, 'u_id'):
        raise InputError(description="Message_id is not a valid message within a \
            channel that the authorised user has joined")
    # check if user has already reacted
    for react in msg['react']:
        if react['u_id'] == u_id:
            raise InputError(description="User has already reacted to this message")
    new_react = {
        'react_id': react_id,
        'u_id': u_id
    }
    for message in data['messages']:
        if message['message_id'] == message_id:
            message['react'].append(new_react)
    return {}

def message_unreact(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of, remove a "react" to \
        that particular message

    Parameters:
        token - The user's token that was generated from their user id

    Returns:
        An empty dictionary

    Errors:
        InputError:
            Message_id is not a valid message within a channel that the authorised user has joined
            React_id is not a valid React ID
            Message with ID message_id does not contain an active React with ID react_id
    '''
    check_token(token)
    data = get_data()
    if react_id != 1:
        raise InputError(description="Invalid React ID")
    if not find_id_in_list(data['messages'], message_id, 'message_id'):
        raise InputError(description="Message_id is not a valid message within a \
            channel that the authorised user has joined")
    for message in data['messages']:
        if message['message_id'] == message_id:
            msg = message
    u_id = get_user_from_token(token)
    channel_id = msg['channel_id']
    curr_channel = data['channels'][channel_id - 1]
    if not find_id_in_list(curr_channel['all_members'], u_id, 'u_id'):
        raise InputError(description="Message_id is not a valid message within a \
            channel that the authorised user has joined")
    # check if user has already reacted
    for react in msg['react']:
        if react['u_id'] == u_id:
            for message in data['messages']:
                if message['message_id'] == message_id:
                    message['react'].remove(react)
                    return {}
    raise InputError(description="User has not reacted to this message")

def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text. If the new message is an empty string, \
        the message is deleted.

    Parameters:
        token - The user's token that was generated from their user id
        message_id - The id of the message to be edited
        message - The edits to be made

    Returns:
        An empty dictionary

    Errors:
        AccessError when none of the following are true:
        Message with message_id was sent by the authorised user making this request
        The authorised user is an owner of this channel or the slackr
    '''
    check_token(token)
    data = get_data()
    if not find_id_in_list(data['messages'], message_id, 'message_id'):
        raise InputError(description="Message does not exist")
    for item in data['messages']:
        if item['message_id'] == message_id:
            msg = item
    u_id = get_user_from_token(token)
    user = data['users'][u_id - 1]
    channel_id = msg['channel_id']
    curr_channel = data['channels'][channel_id - 1]
    is_owner = find_id_in_list(curr_channel['owner_members'], u_id, 'u_id')
    if msg['u_id'] == u_id or user['permission_id'] == 1 or is_owner:
        if message is None:
            message_remove(token, message_id)
            return {}
        for item in data['messages']:
            if item['message_id'] == message_id:
                item['message'] = message
                return {}
    raise AccessError(description='The authorised user does not have privilege to edit message')
