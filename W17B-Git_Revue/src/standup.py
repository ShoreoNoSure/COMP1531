'''
Functions:
    standup_start - Starts a standup
    standup_active - Checks if a standup is active
    standup_send - Sends a message to the standup
'''
import threading
from datetime import datetime, timezone
from helper import check_token, get_data, find_id_in_list, get_user_from_token, send_standup_package
from error import InputError, AccessError

def standup_start(token, channel_id, length):
    '''
    For a given channel, start the standup period whereby for the next "length"
    seconds if someone calls "standup_send" with a message, it is buffered during
    the X second window then at the end of the X second window a message will be
    added to the message queue in the channel from the user who started the standup.
    X is an integer that denotes the number of seconds that the standup occurs for

    Parameters:
        token - The user's token that was generated from their user id
        channel_id - The id of the channel
        length - The length of time in seconds that the standup will last for

    Returns:
        A dictionary containing the time the standup will finish

    Errors:
        InputError:
            Channel ID is not a valid channel
            An active standup is currently running in this channel
    '''
    check_token(token)
    data = get_data()
    # Check if channel_id is valid
    if not find_id_in_list(data['channels'], channel_id, 'channel_id'):
        raise InputError(description="Channel ID is not a valid channel")
    # Check if a standup is already active
    if standup_active(token, channel_id)['is_active']:
        raise InputError(description="An active standup is currently running in this channel")

    standup = data['standup']
    standup['u_id'] = get_user_from_token(token)
    standup['channel_id'] = channel_id
    curr_time = datetime.utcnow()
    time_stamp = int(curr_time.replace(tzinfo=timezone.utc).timestamp())
    standup['time_finish'] = time_stamp + length
    timer = threading.Timer(length, send_standup_package)
    timer.start()
    return {
        'time_finish': standup['time_finish']
    }

def standup_active(token, channel_id):
    '''
    For a given channel, return whether a standup is active in it, and what time
    the standup finishes. If no standup is active, then time_finish returns None

    Parameters:
        token - The user's token that was generated from their user id
        channel_id - The id of the channel

    Returns:
        A dictionary containing the time the standup will finish and whether a
        standup is active

    Errors:
        InputError:
            Channel ID is not a valid channel
    '''
    check_token(token)
    data = get_data()
    # Check if channel_id is valid
    if not find_id_in_list(data['channels'], channel_id, 'channel_id'):
        raise InputError(description="Channel ID is not a valid channel")
    curr_time = datetime.utcnow()
    time_stamp = int(curr_time.replace(tzinfo=timezone.utc).timestamp())
    standup = data['standup']
    if time_stamp > standup['time_finish'] or standup['channel_id'] != channel_id:
        is_active = False
        time_finish = None
    else:
        is_active = True
        time_finish = standup['time_finish']
    return {
        'is_active': is_active,
        'time_finish': time_finish
    }

def standup_send(token, channel_id, message):
    '''
    Sending a message to get buffered in the standup queue, assuming a standup is
    currently active

    Parameters:
        token - The user's token that was generated from their user id
        channel_id - The id of the channel
        message - The message being sent

    Returns:
        A dictionary containing the time the standup will finish and whether a
        standup is active

    Errors:
        InputError:
            Channel ID is not a valid channel
            Message is more than 1000 characters
            An active standup is not currently running in this channel
        AccessError:
            The authorised user is not a member of the channel that the message is within
    '''
    check_token(token)
    data = get_data()
    # Check if channel_id is valid
    if not find_id_in_list(data['channels'], channel_id, 'channel_id'):
        raise InputError(description="Channel ID is not a valid channel")
    # Check if the message is too long
    if len(message) > 1000:
        raise InputError(description="Message is more than 1000 characters")
    # Check if a standup is already active
    if not standup_active(token, channel_id)['is_active']:
        raise InputError(description="An active standup is not currently running in this channel")
    # Check if the user is in the channel
    u_id = get_user_from_token(token)
    curr_channel = data['channels'][channel_id - 1]
    if not find_id_in_list(curr_channel['all_members'], u_id, 'u_id'):
        raise AccessError(description="The authorised user is not a member of the \
        channel that the message is within")
    # Appending the packaged message
    for user in data['users']:
        if user['u_id'] == u_id:
            handle_str = user['handle_str']
    data['standup']['buffer'].append(handle_str + ': ' + message)
    data['standup']['message'] = '\n'.join(data['standup']['buffer'])
    return {
    }
