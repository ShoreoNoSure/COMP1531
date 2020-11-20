#pylint: disable = missing-docstring
import pytest
from auth import auth_register, auth_logout
from other import users_all, search
from user import user_profile_setemail, user_profile_sethandle, user_profile_setname
from channel import channel_join, channel_leave, channel_messages
from channels import channels_create
from message import message_send
from error import AccessError
from helper import reset_data

# ---------------------
# Testing for users_all
# ---------------------

# Test with one user
def test_users_all_simple():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Giving all the users' profile details
    assert users_all(user_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'm@gmail.com',
                'name_first': 'name',
                'name_last': 'lastname',
                'handle_str': 'namelastname',
            }
        ],

    }

# Test with multiple users
def test_users_all_complex():
    reset_data()
    user1_info = auth_register('a@gmail.com', 'sadsad', 'aName', 'aLastname')
    auth_register('b@gmail.com', 'sadsad', 'bName', 'bLastname')
    auth_register('c@gmail.com', 'sadsad', 'cName', 'cLastname')
    # Giving all the users' profile details
    assert users_all(user1_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'a@gmail.com',
                'name_first': 'aName',
                'name_last': 'aLastname',
                'handle_str': 'anamealastname',
            },
            {
                'u_id': 2,
                'email': 'b@gmail.com',
                'name_first': 'bName',
                'name_last': 'bLastname',
                'handle_str': 'bnameblastname',
            },
            {
                'u_id': 3,
                'email': 'c@gmail.com',
                'name_first': 'cName',
                'name_last': 'cLastname',
                'handle_str': 'cnameclastname',
            }
        ],

    }

# Test with a changed name
def test_users_all_newname():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Changing name
    user_profile_setname(user_info['token'], "newname", "newlastname")
    # Giving all the users' profile details
    assert users_all(user_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'm@gmail.com',
                'name_first': 'newname',
                'name_last': 'newlastname',
                'handle_str': 'namelastname',
            }
        ],

    }

# Test with a changed email WIP
def test_users_all_newemail():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Changing email
    user_profile_setemail(user_info['token'], "newm@gmail.com")
    # Giving all the users' profile details
    assert users_all(user_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'newm@gmail.com',
                'name_first': 'name',
                'name_last': 'lastname',
                'handle_str': 'namelastname',
            }
        ],

    }

# Test with a changed handle
def test_users_all_newhandle():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Changing handle
    user_profile_sethandle(user_info['token'], "newhandle")
    # Giving all the users' profile details
    assert users_all(user_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'm@gmail.com',
                'name_first': 'name',
                'name_last': 'lastname',
                'handle_str': 'newhandle',
            }
        ],

    }

# Test when a user has logged out
def test_users_all_logged_out():
    reset_data()
    user1_info = auth_register('a@gmail.com', 'sadsad', 'aName', 'aLastname')
    user2_info = auth_register('b@gmail.com', 'sadsad', 'bName', 'bLastname')
    # User2 logs out
    auth_logout(user2_info['token'])
    # Giving all the users' profile details
    assert users_all(user1_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'a@gmail.com',
                'name_first': 'aName',
                'name_last': 'aLastname',
                'handle_str': 'anamealastname',
            },
            {
                'u_id': 2,
                'email': 'b@gmail.com',
                'name_first': 'bName',
                'name_last': 'bLastname',
                'handle_str': 'bnameblastname',
            },
        ],

    }

# Test with invalid token
def test_users_all_invalid_token():
    reset_data()
    auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Checking if the token is invalid
    with pytest.raises(AccessError):
        users_all('invalidtoken123')

# ------------------
# Testing for search
# ------------------

# Test when there are no messages
def test_search_empty():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Giving all messages containing the query string
    assert search(user_info['token'], "search") == {
        'messages': [
        ],
    }

# Test when there is only no instances of the query string
def test_search_none():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message_send(user_info['token'], 1, "hello there my name is John")
    # Giving all messages containing the query string
    assert search(user_info['token'], "steve") == {
        'messages': [
        ],
    }

# Test when there is only one instance of the query string
def test_search_simple():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message_send(user_info['token'], 1, "hello there my name is John")
    # Finding a timestamp using channel_messages
    tmp = channel_messages(user_info['token'], 1, 0)
    message = tmp['messages'][0]
    timestamp = message['time_created']
    # Giving all messages containing the query string
    assert search(user_info['token'], "hello") == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is John',
                'time_created': timestamp,
            }
        ],
    }

# Test when there are multiple messages containing the query string
def test_search_complex():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message_send(user_info['token'], 1, "hello there my name is John")
    message_send(user_info['token'], 1, "hello John my name is John")
    message_send(user_info['token'], 1, "you aren't John, I'm John")
    # Finding a timestamp
    tmp = channel_messages(user_info['token'], 1, 0)
    message1 = tmp['messages'][2]
    timestamp1 = message1['time_created']
    message2 = tmp['messages'][1]
    timestamp2 = message2['time_created']
    # Giving all messages containing the query string
    assert search(user_info['token'], "hello") == {
        'messages': [
            {
                'message_id': 2,
                'u_id': 1,
                'message': 'hello John my name is John',
                'time_created': timestamp2,
            },
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is John',
                'time_created': timestamp1,
            },
        ],
    }

# Test when there are instances in other people's messages
def test_search_multiple_users():
    reset_data()
    user1_info = auth_register('a@gmail.com', '123456', 'aName', 'aLastname')
    user2_info = auth_register('b@gmail.com', '654321', 'bName', 'bLastname')
    # Creating the channel
    channels_create(user1_info['token'], 'a', True)
    # User 2 joining the channel
    channel_join(user2_info['token'], 1)
    # User 1 & 2 messaging the channel
    message_send(user1_info['token'], 1, "hello there my name is User1")
    message_send(user2_info['token'], 1, "hello User1 my name is User2")
    # Finding a timestamp
    tmp = channel_messages(user2_info['token'], 1, 0)
    message1 = tmp['messages'][1]
    timestamp1 = message1['time_created']
    message2 = tmp['messages'][0]
    timestamp2 = message2['time_created']
    # Giving all messages containing the query string
    assert search(user1_info['token'], "hello") == {
        'messages': [
            {
                'message_id': 2,
                'u_id': 2,
                'message': 'hello User1 my name is User2',
                'time_created': timestamp2,
            },
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is User1',
                'time_created': timestamp1,
            },
        ],
    }

# Test that query string is not case sensitive
def test_search_casesensitive():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message_send(user_info['token'], 1, "hello there my name is John")
    # Finding a timestamp
    tmp = channel_messages(user_info['token'], 1, 0)
    message1 = tmp['messages'][0]
    timestamp1 = message1['time_created']
    # Giving all messages containing the query string
    assert search(user_info['token'], "HELLO") == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is John',
                'time_created': timestamp1,
            }
        ],
    }

# Test when there are multiple channels with instances of the query string
def test_search_multiple_channels():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels_create(user_info['token'], 'a', True)
    channels_create(user_info['token'], 'b', True)
    # Messaging the channel
    message_send(user_info['token'], 1, "hello there my name is John")
    message_send(user_info['token'], 2, "hello there my name is John")
    # Finding a timestamp
    tmp = channel_messages(user_info['token'], 1, 0)
    message1 = tmp['messages'][0]
    timestamp1 = message1['time_created']
    tmp2 = channel_messages(user_info['token'], 2, 0)
    message2 = tmp2['messages'][0]
    timestamp2 = message2['time_created']
    # Giving all messages containing the query string
    assert search(user_info['token'], "hello") == {
        'messages': [
            {
                'message_id': 2,
                'u_id': 1,
                'message': 'hello there my name is John',
                'time_created': timestamp2,
            },
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is John',
                'time_created': timestamp1,
            },
        ],
    }

# Test when you have left the channel with the instance of the query string
def test_search_channel_left():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message_send(user_info['token'], 1, "hello there my name is John")
    # Leaving the channel
    channel_leave(user_info['token'], 1)
    # Giving all messages containing the query string
    assert search(user_info['token'], "hello") == {
        'messages': [
        ],
    }

# Test when there are instances in other channels you are not in
def test_search_excluded():
    reset_data()
    user1_info = auth_register('a@gmail.com', '123456', 'aName', 'aLastname')
    user2_info = auth_register('b@gmail.com', '654321', 'bName', 'bLastname')
    # Creating the channel
    channels_create(user1_info['token'], 'a', True)
    channels_create(user2_info['token'], 'a', True)
    # User 1 & 2 messaging their respective channels
    message_send(user1_info['token'], 1, "hello there my name is User1")
    message_send(user2_info['token'], 2, "hello User1 my name is User2")
    message_send(user1_info['token'], 1, "hello anyone there?")
    # Finding a timestamp
    tmp = channel_messages(user1_info['token'], 1, 0)
    message1 = tmp['messages'][1]
    timestamp1 = message1['time_created']
    message2 = tmp['messages'][0]
    timestamp2 = message2['time_created']
    # Giving all messages containing the query string
    assert search(user1_info['token'], "hello") == {
        'messages': [
            {
                'message_id': 3,
                'u_id': 1,
                'message': 'hello anyone there?',
                'time_created': timestamp2,
            },
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is User1',
                'time_created': timestamp1,
            },
        ],
    }

# Test when the query string is contained within a word
def test_search_query_within():
    reset_data()
    user_info = auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message_send(user_info['token'], 1, "hello there my name is John")
    message_send(user_info['token'], 1, "hello John my name is John")
    message_send(user_info['token'], 1, "you aren't John, I'm John")
    # Finding a timestamp
    tmp = channel_messages(user_info['token'], 1, 0)
    message1 = tmp['messages'][2]
    timestamp1 = message1['time_created']
    message2 = tmp['messages'][1]
    timestamp2 = message2['time_created']
    message3 = tmp['messages'][0]
    timestamp3 = message3['time_created']
    # Giving all messages containing the query string
    assert search(user_info['token'], "o") == {
        'messages': [
            {
                'message_id': 3,
                'u_id': 1,
                'message': "you aren't John, I'm John",
                'time_created': timestamp3,
            },
            {
                'message_id': 2,
                'u_id': 1,
                'message': 'hello John my name is John',
                'time_created': timestamp2,
            },
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is John',
                'time_created': timestamp1,
            },
        ],
    }

# Test with invalid token
def test_search_invalid_token():
    reset_data()
    auth_register('m@gmail.com', 'sadsad', 'name', 'lastname')
    # Checking for invalid token
    with pytest.raises(AccessError):
        search('invalidtoken123', "search")
