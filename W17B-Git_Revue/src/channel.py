#pylint: disable = line-too-long
'''
Functions:
    channel_invite - An authorised person invites a new member to the channel
    channel_details - Show channel details to the authorised person
    channel_addowner - An authorised person adds an owner to the channel's owner list
    channel_removeowner - An authorised person removed an owner from the channel's owner list
    channel_join - An authorised user joins a valid channel
    channel_leave - An authorised user leaves the channel he is in
    channel_messages - An authorised user checks messages in the channel
'''
from operator import itemgetter
from datetime import datetime, timezone
from helper import get_data, get_user_from_token, check_token, find_id_in_list, \
    get_max_u_id, get_user_data
from error import InputError, AccessError


def channel_invite(token, channel_id, u_id):
    '''
    Invite someone to this channel.

    Parameters:
        token -
        channel_id -
        u_id -

    Returns: {}

    Errors:
        InputError:
            Invalid channel id, Invalid u_id.
        AccessError:
            The authorised person is not inside this channel.
    '''
    check_token(token)
    data = get_data()

    if not find_id_in_list(data['channels'], channel_id, 'channel_id'):
        raise InputError(description='Channel does not exist')
    if u_id > get_max_u_id() or u_id <= 0:
        raise InputError(description='u_id does not refer to a valid user')

    current_channel = data['channels'][channel_id - 1]
    person_u_id = get_user_from_token(token)
    # Check if authorised person is in channel with channel_id
    for user in current_channel['all_members']:
        if user['u_id'] == person_u_id:
            target = get_user_data(u_id)
            user_info = {
                'u_id': target['u_id'],
                'name_first': target['name_first'],
                'name_last': target['name_last'],
            }
            data['channels'][channel_id - 1]['all_members'].append(user_info)
            return {}
    # the authorised user is not already a member of the channel
    raise AccessError(description='The authorised user is not a member of this channel')

def channel_details(token, channel_id):
    '''
    Show details to a user.

    Parameters:
        token -
        channel_id -

    Returns: a dict including channel name, owner member list, and member list.

    Errors:
        InputError:
            Invalid channel id.
        AccessError:
            The authorised person is not inside this channel.
    '''
    check_token(token)
    data = get_data()

    if not find_id_in_list(data['channels'], channel_id, 'channel_id'):
        raise InputError(description='Channel does not exist')
    current_channel = data['channels'][channel_id - 1]
    person_u_id = get_user_from_token(token)
    for user in current_channel['all_members']:
        if user['u_id'] == person_u_id:
            for member in current_channel['all_members']:
                info = get_user_data(user['u_id'])
                member['profile_img_url'] = info['profile_img_url']
            # Output { name, owner_members, all_members }
            details = {
                'name': current_channel['name'],
                'owner_members': current_channel['owner_members'],
                'all_members': current_channel['all_members'],
            }
            return details
    raise AccessError(description='he authorised user is not a member of this channel')

def channel_addowner(token, channel_id, u_id):
    '''
    Add a member of channel to owner list.

    Parameters:
        token -
        channel_id -
        u_id -

    Returns: {}

    Errors:
        InputError:
            Invalid channel id.
            User is already an owner.
        AccessError:
            The authorised person is not an owner of channel or owner of slackr.
    '''
    check_token(token)
    data = get_data()
    if not find_id_in_list(data['channels'], channel_id, 'channel_id'):
        raise InputError(description='Channel does not exist')

    current_channel = data['channels'][channel_id - 1]
    if find_id_in_list(current_channel['owner_members'], u_id, 'u_id'):
        raise InputError(description='User is already an owner of this channel')

    person_u_id = get_user_from_token(token)
    person = get_user_data(person_u_id)
    person_is_owner = find_id_in_list(current_channel['owner_members'], person_u_id, 'u_id')
    person_in_channel = find_id_in_list(current_channel['all_members'], person_u_id, 'u_id')
    if person_is_owner or (person_in_channel and person['permission_id'] == 1):
        target = get_user_data(u_id)
        user_info = {
            'u_id': target['u_id'],
            'name_first': target['name_first'],
            'name_last': target['name_last'],
        }
        data['channels'][channel_id - 1]['owner_members'].append(user_info)
        if not find_id_in_list(current_channel['all_members'], u_id, 'u_id'):
            data['channels'][channel_id - 1]['all_members'].append(user_info)
        return {}
    raise AccessError(description='The authorised person has no permission')

def channel_removeowner(token, channel_id, u_id):
    '''
    Remove user from owner list.

    Parameters:
        token -
        channel_id -
        u_id -

    Returns: {}

    Errors:
        InputError:
            Invalid channel id.
            User is not already an owner of the channel.
        AccessError:
            The authorised person is not an owner of channel or owner of slackr.
    '''
    check_token(token)
    data = get_data()
    if not find_id_in_list(data['channels'], channel_id, 'channel_id'):
        raise InputError(description='Channel does not exist')
    current_channel = data['channels'][channel_id - 1]
    if not find_id_in_list(current_channel['owner_members'], u_id, 'u_id'):
        raise InputError(description='User is not an owner of the channel')

    person_u_id = get_user_from_token(token)
    person = get_user_data(person_u_id)
    person_is_owner = find_id_in_list(current_channel['owner_members'], person_u_id, 'u_id')
    person_in_channel = find_id_in_list(current_channel['all_members'], person_u_id, 'u_id')
    if person_is_owner or (person_in_channel and person['permission_id'] == 1):
        target = get_user_data(u_id)
        user_info = {
            'u_id': target['u_id'],
            'name_first': target['name_first'],
            'name_last': target['name_last'],
        }
        data['channels'][channel_id - 1]['owner_members'].remove(user_info)
        return {}
    raise AccessError(description='The authorised person has no permission')

def channel_join(token, channel_id):
    '''
    User joins a channel.

    Parameters:
        token -
        channel_id -

    Returns: {}

    Errors:
        InputError:
            Invalid channel id.
        AccessError:
            Channel is private.
    '''
    check_token(token)
    data = get_data()
    if not find_id_in_list(data['channels'], channel_id, 'channel_id'):
        # Channel ID is not a valid channel
        raise InputError(description='Channel does not exist')
    current_channel = data['channels'][channel_id - 1]

    target_u_id = get_user_from_token(token)
    target = get_user_data(target_u_id)
    if not current_channel['is_public'] and target['permission_id'] != 1:
        raise AccessError(description='Private channel')
    user_info = {
        'u_id': target['u_id'],
        'name_first': target['name_first'],
        'name_last': target['name_last'],
    }
    data['channels'][channel_id - 1]['all_members'].append(user_info)
    return {}

def channel_leave(token, channel_id):
    '''
    User leaves a channel.

    Parameters:
        token -
        channel_id -

    Returns: {}

    Errors:
        InputError:
            Invalid channel id.
        AccessError:
            User is not inside channel.
    '''
    check_token(token)
    data = get_data()
    if not find_id_in_list(data['channels'], channel_id, 'channel_id'):
        raise InputError(description='Channel does not exist')

    current_channel = data['channels'][channel_id - 1]
    target_u_id = get_user_from_token(token)
    if find_id_in_list(current_channel['all_members'], target_u_id, 'u_id'):
        target = get_user_data(target_u_id)
        user_info = {
            'u_id': target['u_id'],
            'name_first': target['name_first'],
            'name_last': target['name_last'],
        }
        data['channels'][channel_id - 1]['all_members'].remove(user_info)
        return {}
    # the authorised user is not a member of channel with channel_id
    raise AccessError(description='The authorised user is not a member of this channel')

def channel_messages(token, channel_id, start):
    '''
    Show message list inside channel to user.

    Parameters:
        token -
        channel_id -
        start -

    Returns:
    {
        'messages': msg_list,
        'start': start,
        'end': end
    }

    Errors:
        InputError:
            Invalid channel id.
            Start is greater than the total number of messages inside channel.
        AccessError:
            User is not inside channel.
    '''
    check_token(token)
    data = get_data()
    if not find_id_in_list(data['channels'], channel_id, 'channel_id'):
        # Channel ID is not a valid channel
        raise InputError(description='Channel does not exist')
    msg_list = []
    curr_time = datetime.utcnow()
    timestamp = curr_time.replace(tzinfo=timezone.utc).timestamp()
    for message in data['messages']:
        if message['channel_id'] == channel_id and message['time_created'] < timestamp:
            tmp_message = {
                'message_id': message['message_id'],
                'u_id': message['u_id'],
                'message': message['message'],
                'time_created': message['time_created']
            }
            msg_list.append(tmp_message)
    msg_list.sort(key=itemgetter('time_created'), reverse=True)
    num_of_messages = len(msg_list)
    start = int(start)
    if start > num_of_messages or start < 0:
        # start is greater than the total number of messages in the channel
        raise InputError(description='Start exceed limit')
    person_u_id = get_user_from_token(token)
    current_channel = data['channels'][channel_id - 1]
    if find_id_in_list(current_channel['all_members'], person_u_id, 'u_id'):
        if start + 49 > num_of_messages:
            end = -1
            msg_list = msg_list[start:]
        # Output { messages, start, end}
        else:
            end = start + 49
            msg_list = msg_list[start:end]
        return {
            'messages': msg_list,
            'start': start,
            'end': end
        }
    # the authorised user is not a member of channel with channel_id
    raise AccessError(description='The authorised user is not a member of this channel')
