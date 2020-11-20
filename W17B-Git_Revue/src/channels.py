'''
Functions:
    channels_create - Creates a channel
    channels_list - Returns a list of channels the user is in
    channels_listall - Returns a list of all channels
'''
from helper import get_data, get_user_from_token, check_token, find_id_in_list
from error import InputError

def channels_create(token, name, is_public):
    '''
    Creates a new channel with that name that is either a public or private channel

    Parameters:
        token - The user's token that was generated from their user id
        name - The name of the channel being created
        is_public - A boolean of whether the channel is public or private

    Returns:
        A dictionary containing the channel_id of the new channel

    Errors:
        InputError:
            The channel name is over 20 characters
    '''
    check_token(token)
    # Raising an error
    if len(name) > 20:
        raise InputError(description='Name is over 20 characters')
    # Getting the channel_id
    data = get_data()
    channel_id = len(data['channels']) + 1
    u_id = get_user_from_token(token)
    # Getting the user details
    for user in data['users']:
        if user['u_id'] == u_id:
            current_user = user
    creator = {
        'u_id': current_user['u_id'],
        'name_first': current_user['name_first'],
        'name_last': current_user['name_last'],
    }

    # Creating a new channel in the class
    new_channel = {
        'name': name,
        'is_public': is_public,
        'owner_members': [creator],
        'all_members': [creator],
        'channel_id': channel_id
    }
    data['channels'].append(new_channel)
    return {
        'channel_id': channel_id
    }

def channels_list(token):
    '''
    Provide a list of all channels (and their associated details) that the authorised
    user is part of

    Parameters:
        token - The user's token that was generated from their user id

    Returns:
        A dictionary containing a list of channels that the user is in

    Errors:
    '''
    check_token(token)
    data = get_data()

    c_list = []
    u_id = get_user_from_token(token)
    # Iterating through the list of channels
    for channel in data['channels']:
        # If the user is in the channel append the channel to the list
        if find_id_in_list(channel['all_members'], u_id, 'u_id'):
            current_channel = {
                'channel_id': channel['channel_id'],
                'name': channel['name'],
            }
            c_list.append(current_channel)
    return {
        'channels': c_list
    }

def channels_listall(token):
    '''
    Provide a list of all channels (and their associated details)

    Parameters:
        token - The user's token that was generated from their user id

    Returns:
        A dictionary containing a list of channels that are public or the user is
        in

    Errors:
    '''
    check_token(token)
    data = get_data()
    c_list = []
    u_id = get_user_from_token(token)
    # Iterating through the list of channels
    for channel in data['channels']:
        # If the user is in the channel append the channel to the list
        if find_id_in_list(channel['all_members'], u_id, 'u_id') or channel['is_public']:
            current_channel = {
                'channel_id': channel['channel_id'],
                'name': channel['name'],
            }
            c_list.append(current_channel)
    return {
        'channels': c_list
    }
