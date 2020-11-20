'''
Functions:
    users_all - Returns a list of all the users
    search - Returns a list of messages that have the word that was searched for
    channels_listall - Returns a list of all channels
'''
from helper import get_data, check_token
from channels import channels_list

def users_all(token):
    '''
    Returns a list of all users and their associated details

    Parameters:
        token - The user's token that was generated from their user id

    Returns:
        A dictionary containing a list of users

    Errors:
    '''
    check_token(token)
    data = get_data()
    u_list = []
    # Adds all the users in data to u_list
    for user in data['users']:
        current_user = {
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
            'profile_img_url': user['profile_img_url'],
        }
        u_list.append(current_user)
    return {
        'users': u_list
    }

def search(token, query_str):
    '''
    Given a query string, return a collection of messages in all of the channels
    that the user has joined that match the query. Results are sorted from most
    recent message to least recent message

    Parameters:
        token - The user's token that was generated from their user id
        query_str - A string that will be searched for

    Returns:
        A dictionary containing a list of messages

    Errors:
    '''
    check_token(token)
    data = get_data()
    channels = channels_list(token)
    m_list = []
    # Iterating through the messages
    for message in data['messages']:
        # Iterating through channels
        for channel in channels['channels']:
            # If the message contains the query string, apppend the dictionary
            if message['channel_id'] == channel['channel_id'] and \
               message['message'].lower().find(query_str.lower()) != -1:
                current_message = {
                    'message_id': message['message_id'],
                    'u_id': message['u_id'],
                    'message': message['message'],
                    'time_created': message['time_created'],
                }
                m_list.append(current_message)
    return {
        'messages': m_list
    }
