#pylint: disable = missing-docstring
import pytest
from auth import auth_register
from channel import channel_addowner, channel_invite, channel_join, channel_leave
from channels import channels_create, channels_list, channels_listall
from error import InputError, AccessError
from helper import reset_data

# ---------------------------
# Testing for channels_create
# ---------------------------

# Test creating a simple channel
def test_channels_create_simple():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating the channel
    assert channels_create(user_info['token'], 'a', True) == {
        'channel_id': 1,
    }
    assert channels_list(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
                'name': 'a'
            }
        ],
    }

# Test creating complexly named channels
def test_channels_create_complex():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating multiple channels
    assert channels_create(user_info['token'], 'C0mpl3x #0ne', True) == {
        'channel_id': 1,
    }
    assert channels_create(user_info['token'], 'C0mpl3x #Tw0', True) == {
        'channel_id': 2,
    }
    assert channels_list(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
                'name': 'C0mpl3x #0ne'
            }, {
                'channel_id': 2,
                'name': 'C0mpl3x #Tw0'
            }
        ]
    }

# Test when channel name has 20 characters
def test_channels_create_success():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')

    assert channels_create(user_info['token'], 'a' * 20, True) == {
        'channel_id': 1
    }
    assert channels_list(user_info['token']) == {
        'channels': [{'channel_id': 1, 'name': 'a' * 20}]}

# Test when the channel has 21 characters
def test_channels_create_fail():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Testing that an error is raised
    with pytest.raises(InputError):
        channels_create(user_info['token'], 'a' * 21, True)

# Test when the channel way too many characters
def test_channels_create_fail_extreme():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Testing that an error is raised
    with pytest.raises(InputError):
        channels_create(user_info['token'], 'a' * 1000000, True)

# Test when the channel is private
def test_channels_create_private():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')

    assert channels_create(user_info['token'], 'Private', False) == {
        'channel_id': 1
    }
    assert channels_list(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1,
                'name': 'Private'
            },
        ],
    }

# Test when multiple users have made channels
def test_channels_create_multiple_users():
    reset_data()
    # Creating multiple users
    user_info1 = auth_register('a@gmail.com', 'sadsad', 'aName', 'aLastname')
    user_info2 = auth_register('b@gmail.com', 'sadsad', 'bName', 'bLastname')
    user_info3 = auth_register('c@gmail.com', 'sadsad', 'cName', 'cLastname')
    # Creating a channel for each user
    assert channels_create(user_info1['token'], 'a', True) == {
        'channel_id': 1
    }
    assert channels_create(user_info2['token'], 'b', True) == {
        'channel_id': 2
    }
    assert channels_create(user_info3['token'], 'c', True) == {
        'channel_id': 3
    }
    assert channels_listall(user_info1['token']) == {
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

# Test with invalid token
def test_channels_create_invalid_token():
    reset_data()
    auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Testing that an error is raised
    with pytest.raises(AccessError):
        channels_create('invalidtoken123', 'a', True)

# -------------------------
# Testing for channels_list
# -------------------------

# Test when user has not created any new channels
def test_channels_list_empty():
    reset_data()
    # Creating the user
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    assert channels_list(user_info['token']) == {
        'channels': [
        ],
    }

# Test when a simple channel has been created
def test_channels_list_simple():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels_create(user_info['token'], 'a', True)
    assert channels_list(user_info['token']) == {
        'channels': [{'channel_id': 1, 'name': 'a'}]}

# Test when complex channels have been created
def test_channels_list_complex():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating multiple channels
    channels_create(user_info['token'], 'C0mpl3x #0ne', True)
    channels_create(user_info['token'], 'C0mpl3x #Tw0', True)
    assert channels_list(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'C0mpl3x #0ne'
            }, {
                'channel_id': 2, 'name': 'C0mpl3x #Tw0'
            }
        ]
    }

# Test when two channels have the same name
def test_channels_list_same():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')

    channels_create(user_info['token'], 'a', True)
    channels_create(user_info['token'], 'a', True)
    assert channels_list(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'a'
            }, {
                'channel_id': 2, 'name': 'a'
            }
        ]
    }

# Test when one channel the user has created is private
def test_channels_list_private():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')

    channels_create(user_info['token'], 'Private', False)
    channels_create(user_info['token'], 'Public', True)
    assert channels_list(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'Private'
            }, {
                'channel_id': 2, 'name': 'Public'
            }
        ]
    }

# Test when a user is not part of a private channel
def test_channels_list_private_excluded():
    reset_data()
    # Creating multiple users
    user1_info = auth_register('a@gmail.com', 'sadsad', 'aName', 'aLastname')
    user2_info = auth_register('b@gmail.com', 'sadsad', 'bName', 'bLastname')

    channels_create(user1_info['token'], 'Private', False)

    assert channels_list(user2_info['token']) == {'channels': []}

# Test when a user is invited to a private channel
def test_channels_list_private_included():
    reset_data()
    user1_info = auth_register('a@gmail.com', 'sadsad', 'aName', 'aLastname')
    user2_info = auth_register('b@gmail.com', 'sadsad', 'bName', 'bLastname')

    channels_create(user2_info['token'], 'Private', False)
    # Inviting a user to a channel
    channel_invite(user2_info['token'], 1, user1_info['u_id'])

    assert channels_list(user1_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'Private'
            }
        ]
    }

# Test when a user is made owner of a private channel
def test_channels_list_private_newowner():
    reset_data()
    user1_info = auth_register('a@gmail.com', 'sadsad', 'aName', 'aLastname')
    user2_info = auth_register('b@gmail.com', 'sadsad', 'bName', 'bLastname')

    channels_create(user2_info['token'], 'Private', False)
    # Making a user owner of a channel
    channel_addowner(user2_info['token'], 1, user1_info['u_id'])

    assert channels_list(user1_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'Private'
            }
        ]
    }

# Test when a user is not part of a public channel
def test_channels_list_public_excluded():
    reset_data()
    # Creating multiple users
    user1_info = auth_register('a@gmail.com', 'sadsad', 'aName', 'aLastname')
    user2_info = auth_register('b@gmail.com', 'sadsad', 'bName', 'bLastname')

    channels_create(user1_info['token'], 'Public', True)

    assert channels_list(user2_info['token']) == {
        'channels': []
    }

# Test when a user has joined a public channel
def test_channels_list_public_included():
    # Creating multiple users
    reset_data()
    user1_info = auth_register('a@gmail.com', 'sadsad', 'aName', 'aLastname')
    user2_info = auth_register('b@gmail.com', 'sadsad', 'bName', 'bLastname')

    channels_create(user1_info['token'], 'Public', True)
    # Joining the channel
    channel_join(user2_info['token'], 1)

    assert channels_list(user2_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'Public'
            }
        ]
    }

# Test when a user has left a channel
def test_channels_list_left():
    reset_data()
    # Creating multiple users
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')

    channels_create(user_info['token'], 'Public', True)
    # Leaving the channel
    channel_leave(user_info['token'], 1)

    assert channels_list(user_info['token']) == {
        'channels': []
    }

# Test with invalid token
def test_channels_list_invalid_token():
    reset_data()
    auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Testing that an error is raised
    with pytest.raises(AccessError):
        channels_list('invalidtoken123')

# ----------------------------
# Testing for channels_listall
# ----------------------------

# Test when user has not created any new channels
def test_channels_listall_empty():
    reset_data()
    # Creating the user
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    assert channels_listall(user_info['token']) == {
        'channels': [
        ],
    }

# Test when a simple channel has been created
def test_channels_listall_simple():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels_create(user_info['token'], 'a', True)
    assert channels_listall(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'a'
            }
        ],
    }

# Test when complex channels have been created
def test_channels_listall_complex():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating multiple channels
    channels_create(user_info['token'], 'C0mpl3x #0ne', True)
    channels_create(user_info['token'], 'C0mpl3x #Tw0', True)
    assert channels_listall(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'C0mpl3x #0ne'
            }, {
                'channel_id': 2, 'name': 'C0mpl3x #Tw0'
            }
        ]
    }

# Test when two channels have the same name
def test_channels_listall_same():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')

    channels_create(user_info['token'], 'a', True)
    channels_create(user_info['token'], 'a', True)
    assert channels_listall(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'a'
            }, {
                'channel_id': 2, 'name': 'a'
            }
        ]
    }

# Test when one channel the user has created is private
def test_channels_listall_private():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')

    channels_create(user_info['token'], 'Private', False)
    channels_create(user_info['token'], 'Public', True)
    assert channels_listall(user_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'Private'
            }, {
                'channel_id': 2, 'name': 'Public'
            }
        ]
    }

# Test when a user is not part of a private channel
def test_channels_listall_private_excluded():
    reset_data()
    # Creating multiple users
    user1_info = auth_register('a@gmail.com', 'sadsad', 'aName', 'aLastname')
    user2_info = auth_register('b@gmail.com', 'sadsad', 'bName', 'bLastname')

    channels_create(user1_info['token'], 'Private', False)
    channels_create(user1_info['token'], 'Public', True)

    assert channels_listall(user2_info['token']) == {
        'channels': [
            {
                'channel_id': 2, 'name': 'Public'
            }
        ]
    }

# Test when a user is invited to a private channel
def test_channels_listall_private_included():
    reset_data()
    user1_info = auth_register('a@gmail.com', 'sadsad', 'aName', 'aLastname')
    user2_info = auth_register('b@gmail.com', 'sadsad', 'bName', 'bLastname')
    channels_create(user2_info['token'], 'Private', False)
    channels_create(user2_info['token'], 'Public', True)
    # Inviting a user to a channel
    channel_invite(user2_info['token'], 1, user1_info['u_id'])

    assert channels_listall(user1_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'Private'
            },
            {
                'channel_id': 2, 'name': 'Public'
            }
        ],
    }

# Test when a user is made owner of a private channel
def test_channels_listall_private_newowner():
    reset_data()
    user1_info = auth_register('a@gmail.com', 'sadsad', 'aName', 'aLastname')
    user2_info = auth_register('b@gmail.com', 'sadsad', 'bName', 'bLastname')

    channels_create(user2_info['token'], 'Private', False)
    channels_create(user2_info['token'], 'Public', True)
    # Making a user owner of a channel
    channel_addowner(user2_info['token'], 1, user1_info['u_id'])

    assert channels_listall(user1_info['token']) == {
        'channels': [
            {
                'channel_id': 1, 'name': 'Private'
            },
            {
                'channel_id': 2, 'name': 'Public'
            }
        ],
    }

# Test when a user has left a private channel
def test_channels_listall_private_left():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    channels_create(user_info['token'], 'Private', False)
    channels_create(user_info['token'], 'Public', True)
    # Leaving a channel
    channel_leave(user_info['token'], 1)

    assert channels_listall(user_info['token']) == {
        'channels': [
            {
                'channel_id': 2, 'name': 'Public'
            }
        ]
    }

# Test with invalid token
def test_channels_listall_invalid_token():
    reset_data()
    auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Testing that an error is raised
    with pytest.raises(AccessError):
        channels_listall('invalidtoken123')
