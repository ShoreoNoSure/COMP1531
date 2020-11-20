import auth
import channel
import channels
import pytest

# Test when user has not created any new channels
def test_channels_listall_empty():
    # Creating the user
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    assert channels.channels_listall(user_info['token']) == {
        'channels': [
        ],
    }

# Test when a simple channel has been created
def test_channels_listall_simple():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels.channels_create(user_info['token'], 'a', True)
    assert channels.channels_listall(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
        		'name': 'a',
            }
        ],
    }

# Test when complex channels have been created
def test_channels_listall_complex():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Creating multiple channels
    channels.channels_create(user_info['token'], 'C0mpl3x #0ne', True)
    channels.channels_create(user_info['token'], 'C0mpl3x #Tw0', True)
    assert channels.channels_listall(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
        		'name': 'C0mpl3x #0ne',
            },
            {
                'channel_id': 2,
        		'name': 'C0mpl3x #Tw0',
            }
        ],
    }

# Test when two channels have the same name
def test_channels_listall_same():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')

    channels.channels_create(user_info['token'], 'a', True)
    channels.channels_create(user_info['token'], 'a', True)
    assert channels.channels_listall(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
        		'name': 'a',
            },
            {
                'channel_id': 2,
        		'name': 'a',
            }
        ],
    }

# Test when one channel the user has created is private
def test_channels_listall_private():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')

    channels.channels_create(user_info['token'], 'Private', False)
    channels.channels_create(user_info['token'], 'Public', True)
    assert channels.channels_listall(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
        		'name': 'Private',
            },
            {
                'channel_id': 2,
        		'name': 'Public',
            }
        ],
    }

# Test when a user is not part of a private channel
def test_channels_listall_private_excluded():
    # Creating multiple users
    user1_info = auth.auth_register('a@gmail', 'sadsad', 'aName', 'aLastname')
    user2_info = auth.auth_register('b@gmail', 'sadsad', 'bName', 'bLastname')

    channels.channels_create(user1_info['token'], 'Private', False)
    channels.channels_create(user1_info['token'], 'Public', True)

    assert channels.channels_listall(user2_info['token']) == {
        'channels': [
            {
                'channel_id': 2,
        		'name': 'Public',
            }
        ],
    }

# Test when a user is invited to a private channel
def test_channels_listall_private_included():
    user1_info = auth.auth_register('a@gmail', 'sadsad', 'aName', 'aLastname')
    user2_info = auth.auth_register('b@gmail', 'sadsad', 'bName', 'bLastname')

    channels.channels_create(user2_info['token'], 'Private', False)
    channels.channels_create(user2_info['token'], 'Public', True)
    # Inviting a user to a channel
    channel.channel_invite(user2_info['token'], 1, user1_info['u_id'])

    assert channels.channels_listall(user1_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
        		'name': 'Private',
            },
            {
                'channel_id': 2,
        		'name': 'Public',
            }
        ],
    }

# Test when a user is made owner of a private channel
def test_channels_listall_private_newowner():
    user1_info = auth.auth_register('a@gmail', 'sadsad', 'aName', 'aLastname')
    user2_info = auth.auth_register('b@gmail', 'sadsad', 'bName', 'bLastname')

    channels.channels_create(user2_info['token'], 'Private', False)
    channels.channels_create(user2_info['token'], 'Public', True)
    # Making a user owner of a channel
    channel.channel_addowner(user2_info['token'], 1, user1_info['u_id'])

    assert channels.channels_listall(user1_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
        		'name': 'Private',
            },
            {
                'channel_id': 2,
        		'name': 'Public',
            }
        ],
    }

# Test when a user has left a private channel
def test_channels_listall_private_left():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')

    channels.channels_create(user_info['token'], 'Private', False)
    channels.channels_create(user_info['token'], 'Public', True)
    # Leaving a channel
    channel.channel_leave(user_info['token'], 1)
    
    assert channels.channels_listall(user_info['token']) == {
        'channels': [
            {
                'channel_id': 2,
        		'name': 'Public',
            }
        ],
    }
