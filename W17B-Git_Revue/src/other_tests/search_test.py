import auth
import other
import channel
import channels
import message
import datetime
import pytest

# Test when there are no messages
def test_search_empty():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Giving all messages containing the query string
    assert other.search(user_info['token'], "search") == {
        'messages': [
        ],
    }

# Test when there is only no instances of the query string
def test_search_none():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels.channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message.message_send(user_info['token'], 1, "hello there my name is John")
    # Giving all messages containing the query string
    assert other.search(user_info['token'], "steve") == {
        'messages': [
        ],
    }

# Test when there is only one instance of the query string
def test_search_simple():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels.channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message.message_send(user_info['token'], 1, "hello there my name is John")
    # Finding a timestamp using channel_messages
    tmp = channel.channel_messages(user_info['token'], 1, 0)
    message = tmp['messages'][0]
    timestamp = message['time_created']
    # Giving all messages containing the query string
    assert other.search(user_info['token'], "hello") == {
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
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels.channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message.message_send(user_info['token'], 1, "hello there my name is John")
    message.message_send(user_info['token'], 1, "hello John my name is John")
    message.message_send(user_info['token'], 1, "you aren't John, I'm John")
    # Finding a timestamp
    tmp = channel.channel_messages(user_info['token'], 1, 0)
    message1 = tmp['messages'][0]
    timestamp1 = message1['time_created']
    message2 = tmp['messages'][1]
    timestamp2 = message2['time_created']
    # Giving all messages containing the query string
    assert other.search(user_info['token'], "hello") == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is John',
                'time_created': timestamp1,
            },
            {
                'message_id': 2,
                'u_id': 1,
                'message': 'hello John my name is John',
                'time_created': timestamp2,
            }
        ],
    }

# Test when there are instances in other people's messages
def test_search_multiple_users():
    user1_info = auth.auth_register('a@gmail', '123', 'aName', 'aLastname')
    user2_info = auth.auth_register('b@gmail', '321', 'bName', 'bLastname')
    # Creating the channel
    channels.channels_create(user1_info['token'], 'a', True)
    # User 2 joining the channel
    channel.channel_join(user2_info['token'], 1)
    # User 1 & 2 messaging the channel
    message.message_send(user1_info['token'], 1, "hello there my name is User1")
    message.message_send(user2_info['token'], 1, "hello User1 my name is User2")
    # Finding a timestamp
    tmp = channel.channel_messages(user2_info['token'], 1, 0)
    message1 = tmp['messages'][0]
    timestamp1 = message1['time_created']
    message2 = tmp['messages'][1]
    timestamp2 = message2['time_created']
    # Giving all messages containing the query string
    assert other.search(user1_info['token'], "hello") == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is User1',
                'time_created': timestamp1,
            },
            {
                'message_id': 2,
                'u_id': 2,
                'message': 'hello User1 my name is User2',
                'time_created': timestamp2,
            }
        ],
    }

# Test that query string is not case sensitive
def test_search_casesensitive():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels.channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message.message_send(user_info['token'], 1, "hello there my name is John")
    # Finding a timestamp
    tmp = channel.channel_messages(user_info['token'], 1, 0)
    message1 = tmp['messages'][0]
    timestamp1 = message1['time_created']
    # Giving all messages containing the query string
    assert other.search(user_info['token'], "HELLO") == {
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
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels.channels_create(user_info['token'], 'a', True)
    channels.channels_create(user_info['token'], 'b', True)
    # Messaging the channel
    message.message_send(user_info['token'], 1, "hello there my name is John")
    message.message_send(user_info['token'], 2, "hello there my name is John")
    # Finding a timestamp
    tmp = channel.channel_messages(user_info['token'], 1, 0)
    message1 = tmp['messages'][0]
    timestamp1 = message1['time_created']
    tmp2 = channel.channel_messages(user_info['token'], 2, 0)
    message2 = tmp2['messages'][0]
    timestamp2 = message2['time_created']
    # Giving all messages containing the query string
    assert other.search(user_info['token'], "hello") == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is John',
                'time_created': timestamp1,
            },
            {
                'message_id': 2,
                'u_id': 1,
                'message': 'hello there my name is John',
                'time_created': timestamp2,
            }
        ],
    }

# Test when you have left the channel with the instance of the query string
def test_search_channel_left():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels.channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message.message_send(user_info['token'], 1, "hello there my name is John")
    # Leaving the channel
    channel.channel_leave(user_info['token'], 1)
    # Giving all messages containing the query string
    assert other.search(user_info['token'], "hello") == {
        'messages': [
        ],
    }

# Test when there are instances in other channels you are not in
def test_search_excluded():
    user1_info = auth.auth_register('a@gmail', '123', 'aName', 'aLastname')
    user2_info = auth.auth_register('b@gmail', '321', 'bName', 'bLastname')
    # Creating the channel
    channels.channels_create(user1_info['token'], 'a', True)
    channels.channels_create(user2_info['token'], 'a', True)
    # User 1 & 2 messaging their respective channels
    message.message_send(user1_info['token'], 1, "hello there my name is User1")
    message.message_send(user2_info['token'], 2, "hello User1 my name is User2")
    message.message_send(user1_info['token'], 1, "hello anyone there?")
    # Finding a timestamp
    tmp = channel.channel_messages(user1_info['token'], 1, 0)
    message1 = tmp['messages'][0]
    timestamp1 = message1['time_created']
    message2 = tmp['messages'][1]
    timestamp2 = message2['time_created']
    # Giving all messages containing the query string
    assert other.search(user1_info['token'], "hello") == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is User1',
                'time_created': timestamp1,
            },
            {
                'message_id': 3,
                'u_id': 1,
                'message': 'hello anyone there?',
                'time_created': timestamp2,
            }
        ],
    }

# Test when the query string is contained within a word
def test_search_query_within():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Creating the channel
    channels.channels_create(user_info['token'], 'a', True)
    # Messaging the channel
    message.message_send(user_info['token'], 1, "hello there my name is John")
    message.message_send(user_info['token'], 1, "hello John my name is John")
    message.message_send(user_info['token'], 1, "you aren't John, I'm John")
    # Finding a timestamp
    tmp = channel.channel_messages(user_info['token'], 1, 0)
    message1 = tmp['messages'][0]
    timestamp1 = message1['time_created']
    message2 = tmp['messages'][1]
    timestamp2 = message2['time_created']
    message3 = tmp['messages'][2]
    timestamp3 = message3['time_created']
    # Giving all messages containing the query string
    assert other.search(user_info['token'], "o") == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'hello there my name is John',
                'time_created': timestamp1,
            },
            {
                'message_id': 2,
                'u_id': 1,
                'message': 'hello John my name is John',
                'time_created': timestamp2,
            },
            {
                'message_id': 3,
                'u_id': 1,
                'message': "you aren't John, I'm John",
                'time_created': timestamp3,
            }
        ],
    }
