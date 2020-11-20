#pylint: disable = missing-docstring
from time import sleep
import pytest
from auth import auth_register
from channel import channel_join, channel_messages
from channels import channels_create
from standup import standup_active, standup_start, standup_send
from helper import reset_data
from error import InputError, AccessError

# -------------------------
# Testing for standup_start
# -------------------------

# Test empty standup
def test_standup_start_empty():
    reset_data()
    member = auth_register('example@gmail.com', 'helloworld', 'Roy', 'Wallace')
    test_channel = channels_create(member['token'], 'New Channel', True)
    channel_id = test_channel['channel_id']

    standup_start(member['token'], channel_id, 1)
    sleep(1.1)
    assert channel_messages(member['token'], channel_id, 0) == {
        'messages': [],
        'start': 0,
        'end': -1,
        }

# Test simple standup with one message
def test_standup_start_simple():
    reset_data()
    member = auth_register('example@gmail.com', 'helloworld', 'Roy', 'Wallace')
    test_channel = channels_create(member['token'], 'New Channel', True)
    channel_id = test_channel['channel_id']

    standup_start(member['token'], channel_id, 1)
    standup_send(member['token'], channel_id, 'Standup message')
    sleep(1.1)
    tmp = channel_messages(member['token'], channel_id, 0)
    message = tmp['messages'][0]
    timestamp = message['time_created']
    assert channel_messages(member['token'], channel_id, 0) == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'roywallace: Standup message',
                'time_created': timestamp
            }],
        'start': 0,
        'end': -1,
        }

# Test standup with two messages from two different people
def test_standup_start_complex():
    reset_data()
    member1 = auth_register('exampleA@gmail.com', 'helloworld', 'ARoy', 'Wallace')
    member2 = auth_register('exampleB@gmail.com', 'helloworld', 'BRoy', 'Wallace')
    test_channel = channels_create(member1['token'], 'New Channel', True)
    channel_id = test_channel['channel_id']
    channel_join(member2['token'], channel_id)

    standup_start(member2['token'], channel_id, 1)
    standup_send(member1['token'], channel_id, 'Standup message1')
    standup_send(member2['token'], channel_id, 'Standup message2')
    sleep(1.1)
    tmp = channel_messages(member1['token'], channel_id, 0)
    message = tmp['messages'][0]
    timestamp = message['time_created']
    assert channel_messages(member2['token'], channel_id, 0) == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 2,
                'message': 'aroywallace: Standup message1\nbroywallace: Standup message2',
                'time_created': timestamp
            },
            ],
        'start': 0,
        'end': -1,
        }

# Test when channel_id is invalid
def test_standup_start_invalid_channel_id():
    reset_data()
    member = auth_register('example@gmail.com', 'helloworld', 'firstname', 'lastname')
    channels_create(member['token'], 'New Channel', True)
    with pytest.raises(InputError):
        standup_start(member['token'], 2, 10)

# Test when standup is already active
def test_standup_start_already_active():
    reset_data()
    member1 = auth_register('example@gmail.com', 'helloworld', 'firstname', 'lastname')
    test_channel = channels_create(member1['token'], 'New Channel', True)
    standup_start(member1['token'], test_channel['channel_id'], 10)

    with pytest.raises(InputError):
        standup_start(member1['token'], test_channel['channel_id'], 6)

# --------------------------
# Testing for standup_active
# --------------------------

# Test when standup is active
def test_standup_active_active():
    reset_data()
    member = auth_register('example@gmail.com', 'helloworld', 'firstname', 'lastname')
    channel_id = channels_create(member['token'], 'New Channel', True)['channel_id']
    standup = standup_start(member['token'], channel_id, 5)

    assert standup_active(member['token'], channel_id) == {
        'is_active': True,
        'time_finish': standup['time_finish']
    }

# Test when standup is inactive
def test_standup_active_inactive():
    reset_data()
    member = auth_register('example@gmail.com', 'helloworld', 'firstname', 'lastname')
    channel_id = channels_create(member['token'], 'New Channel', True)['channel_id']

    assert standup_active(member['token'], channel_id) == {
        'is_active': False,
        'time_finish': None
    }

# Test when channel_id is invalid
def test_standup_active_invalid_channel_id():
    reset_data()
    member1 = auth_register('example@gmail.com', 'helloworld', 'firstname', 'lastname')
    channels_create(member1['token'], 'New Channel', True)
    with pytest.raises(InputError):
        standup_active(member1['token'], 2)

# Test when standup is active in another channel
def test_standup_active_wrong_channel():
    reset_data()
    member = auth_register('example@gmail.com', 'helloworld', 'firstname', 'lastname')
    channel_id1 = channels_create(member['token'], 'Channel One', True)['channel_id']
    channel_id2 = channels_create(member['token'], 'Channel Two', True)['channel_id']
    standup_start(member['token'], channel_id1, 1)

    assert standup_active(member['token'], channel_id2) == {
        'is_active': False,
        'time_finish': None
    }

# ------------------------
# Testing for standup_send
# ------------------------

# Test for simple standup messages
def test_standup_send_simple():
    reset_data()
    member1 = auth_register('example@gmail.com', 'helloworld', 'a', 'A')
    member2 = auth_register('jiaqizhu@gmail.com', 'thisisfun', 'b', 'B')
    member3 = auth_register('robbie@hotmail.com', 'iamrobbie', 'c', 'C')
    channel = channels_create(member1['token'], 'Hey Channel', True)
    channel_id = channel['channel_id']
    channel_join(member2['token'], channel_id)
    channel_join(member3['token'], channel_id)
    standup_start(member1['token'], channel_id, 1)
    assert standup_send(member1['token'], channel_id, '1') == {}
    assert standup_send(member2['token'], channel_id, '2') == {}
    assert standup_send(member3['token'], channel_id, '3') == {}
    sleep(1.1)
    tmp = channel_messages(member1['token'], channel_id, 0)
    message = tmp['messages'][0]
    timestamp = message['time_created']
    assert channel_messages(member1['token'], channel_id, 0) == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'aa: 1\nbb: 2\ncc: 3',
                'time_created': timestamp
            },
            ],
        'start': 0,
        'end': -1,
        }

# Test for complex standup messages
def test_standup_send_complex():
    reset_data()
    member1 = auth_register('example@gmail.com', 'helloworld', 'a', 'A')
    member2 = auth_register('jiaqizhu@gmail.com', 'thisisfun', 'b', 'B')
    member3 = auth_register('robbie@hotmail.com', 'iamrobbie', 'c', 'C')
    channel = channels_create(member1['token'], 'Hey Channel', True)
    channel_id = channel['channel_id']
    channel_join(member2['token'], channel_id)
    channel_join(member3['token'], channel_id)
    standup_start(member1['token'], channel_id, 1)
    assert standup_send(member1['token'], channel_id, '1\nSTOP') == {}
    assert standup_send(member2['token'], channel_id, '2\nSTOP') == {}
    assert standup_send(member3['token'], channel_id, '3\nSTOP') == {}
    sleep(1.1)
    tmp = channel_messages(member1['token'], channel_id, 0)
    message = tmp['messages'][0]
    timestamp = message['time_created']
    assert channel_messages(member1['token'], channel_id, 0) == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'aa: 1\nSTOP\nbb: 2\nSTOP\ncc: 3\nSTOP',
                'time_created': timestamp
            },
            ],
        'start': 0,
        'end': -1,
        }

# Test for invalid channel_id
def test_standup_send_invalid_channel_id():
    reset_data()
    member = auth_register('example@gmail.com', 'helloworld', 'firstname', 'lastname')
    channel_id = channels_create(member['token'], 'Channel', True)
    standup_start(member['token'], channel_id['channel_id'], 3)

    with pytest.raises(InputError):
        standup_send(member['token'], 2, 'hello')

def test_standup_send_long_message():
    reset_data()
    member = auth_register('example@gmail.com', 'helloworld', 'firstname', 'lastname')
    channel_id = channels_create(member['token'], 'Channel', True)
    standup_start(member['token'], channel_id['channel_id'], 3)

    with pytest.raises(InputError):
        standup_send(member['token'], 1, 'a'*1001)

def test_standup_send_no_active_standup():
    reset_data()
    member = auth_register('example@gmail.com', 'helloworld', 'firstname', 'lastname')
    channels_create(member['token'], 'Channel', True)

    with pytest.raises(InputError):
        standup_send(member['token'], 1, 'a')

def test_standup_send_user_not_in_channel():
    reset_data()
    member1 = auth_register('a@gmail.com', 'helloworld', 'a', 'A')
    member2 = auth_register('b@gmail.com', 'helloworld', 'b', 'B')
    channel_id = channels_create(member1['token'], 'Channel', True)
    standup_start(member1['token'], channel_id['channel_id'], 3)

    with pytest.raises(AccessError):
        standup_send(member2['token'], 1, 'a')
