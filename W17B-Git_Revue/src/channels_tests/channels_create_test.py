import auth
import channel
import channels
from error import InputError
import pytest

# Test creating a simple channel
def test_channels_create_simple():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Creating the channel
    assert channels.channels_create(user_info['token'], 'a', True) == {
        'channel_id': 1, 
    }
    assert channels.channels_list(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
        		'name': 'a',
            }
        ],
    }

# Test creating complexly named channels
def test_channels_create_complex():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Creating multiple channels
    assert channels.channels_create(user_info['token'], 'C0mpl3x #0ne', True) == {
        'channel_id': 1, 
    }
    assert channels.channels_create(user_info['token'], 'C0mpl3x #Tw0', True) == {
        'channel_id': 2, 
    }
    assert channels.channels_list(user_info['token']) == {
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

# Test when channel name has 20 characters
def test_channels_create_success():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')

    assert channels.channels_create(user_info['token'], 'a' * 20, True) == {
        'channel_id': 1, 
    }
    assert channels.channels_list(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
        		'name': 'a' * 20,
            },
        ],
    }

# Test when the channel has 21 characters
def test_channels_create_fail():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Testing that an error is raised
    with pytest.raises(InputError) as e:
        channels.channels_create(user_info['token'], 'a' * 21, True)

# Test when the channel way too many characters
def test_channels_create_fail_extreme():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Testing that an error is raised
    with pytest.raises(InputError) as e:
        channels.channels_create(user_info['token'], 'a' * 1000000, True)

# Test when the channel is private
def test_channels_create_private():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')

    assert channels.channels_create(user_info['token'], 'Private', False) == {
        'channel_id': 1, 
    }
    assert channels.channels_list(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
                'name': 'Private',
            },
        ],
    }

# Test when multiple users have made channels
def test_channels_create_multiple_users():
    # Creating multiple users
    user_info1 = auth.auth_register('a@gmail', 'sadsad', 'aName', 'aLastname')
    user_info2 = auth.auth_register('b@gmail', 'sadsad', 'bName', 'bLastname')
    user_info3 = auth.auth_register('c@gmail', 'sadsad', 'cName', 'cLastname')
    # Creating a channel for each user
    assert channels.channels_create(user_info1['token'], 'a', True) == {
        'channel_id': 1, 
    }
    assert channels.channels_create(user_info2['token'], 'b', True) == {
        'channel_id': 2, 
    }
    assert channels.channels_create(user_info3['token'], 'c', True) == {
        'channel_id': 3, 
    }
    assert channels.channels_listall(user_info1['token']) == {
        'channels': [
            {
                'channel_id': 1,
                'name': 'a',
            },
            {
                'channel_id': 2,
                'name': 'b',
            },
            {
                'channel_id': 3,
                'name': 'c',
            },
        ],
    }