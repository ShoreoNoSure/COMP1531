from werkzeug.exceptions import HTTPException
import urllib
import urllib.request
from datetime import datetime, timezone
from time import sleep, time
import json
import pytest
from helper import get_data, find_id_in_list, check_token, get_handle, hash_password

BASE_URL = "http://127.0.0.1:8000"

# ----------
# Auth Tests
# ----------

def test_auth_register():
    '''test successful registration'''
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    data = json.dumps({"email": "jiaqi@gmail.com", "password": hash_password("ilovecse"), "name_first": "Jiaqi", "name_last": "Zhu"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token = payload["token"]
    
    response = urllib.request.urlopen(f"{BASE_URL}/users/all?token={token}")
    payload = json.load(response)
    assert payload == {
        "users": [{
            "u_id": 1,
            "email": "jiaqi@gmail.com",
            "name_first": "Jiaqi",
            "name_last": "Zhu",
            "handle_str":get_handle("Jiaqi", "Zhu"),
        }]
    }

def test_empty_email():
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    data = json.dumps({"email": None, "password": hash_password("helloworld"), "name_first": "Kool", "name_last": "Name"}).encode("utf-8")
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=data,
            headers={"Content-Type": "application/json"},
            method='POST'
        ))

def test_empty_password():
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    data = json.dumps({"email": "koolname@hotmail.com", "password": "", "name_first": "Kool", "name_last": "Name"}).encode("utf-8")
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=data,
            headers={"Content-Type": "application/json"},
            method='POST'
        ))

def test_empty_first_name():
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    data = json.dumps({"email": "koolname@hotmail.com", "password": hash_password("helloworld"), "name_first": "", "name_last": "Name"}).encode("utf-8")
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=data,
            headers={"Content-Type": "application/json"},
            method='POST'
        ))

def test_empty_last_name():
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    data = json.dumps({"email": "koolname@hotmail.com", "password": hash_password("helloworld"), "name_first": "Kool", "name_last": ""}).encode("utf-8")
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=data,
            headers={"Content-Type": "application/json"},
            method='POST'
        ))
    
def test_auth_logout():
    '''testing if user can successfully logout'''
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    data = json.dumps({"email": "jiaqi@gmail.com", "password": hash_password("ilovecse"), "name_first": "Jiaqi", "name_last": "Zhu"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token = payload['token']
    token = json.dumps(token).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/logout",
        data=token,
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        payload = json.load(response)
    assert payload == {"is_success": True}

def test_auth_login():
    '''test successful login'''
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    data = json.dumps({"email": "jiaqi@gmail.com", "password": hash_password("ilovecse"), "name_first": "Jiaqi", "name_last": "Zhu"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token = payload['token']
    u_id = payload['u_id']
    token = json.dumps(token).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/logout",
        data=token,
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        payload = json.load(response)
    data = json.dumps({"email": "jiaqi@gmail.com", "password": hash_password("ilovecse")}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/login",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        payload = json.load(response)
    assert payload['u_id'] == u_id

# -------------
# Channel Tests
# -------------

def test_channel_details():
    '''test successful return of channel details'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token = payload["token"]
    u_id = payload["u_id"]
    #create a new channel
    data = json.dumps({"token": token, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id = payload["channel_id"]
    #chcking that the channel details are correct
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token}&channel_id={channel_id}")
    payload = json.load(response)
    assert payload == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            }
        ],
        'all_members': [
            {
                'u_id': u_id,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
        ],
    }

def test_channel_invite():
    '''test successful invite of another user to a channel
    also tests channel detales '''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token = payload["token"]
    u_id1 = payload["u_id"]
    #create a new channel
    data = json.dumps({"token": token, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id = payload["channel_id"]
    #create a second user
    data = json.dumps({"email": "sinhanawa@gmail.com", "password": hash_password("ilovecse"), "name_first": "Sinha", "name_last": "Nawa"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    u_id2 = payload["u_id"]
    #inviting second user to the channel
    data = json.dumps({"token": token, "channel_id": channel_id, "u_id": u_id2}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/invite",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #chcking that the second user was invited to the channel
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token}&channel_id={channel_id}")
    payload = json.load(response)
    assert payload == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            }
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
            {
                'u_id': u_id2,
                'name_first': 'Sinha',
                'name_last': 'Nawa',
            }
        ],
    }

def test_channel_join():
    '''test successful invite of another user to a channel
    also tests channel detales'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token = payload["token"]
    u_id1 = payload["u_id"]
    #create a new channel
    data = json.dumps({"token": token, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id = payload["channel_id"]
    #create a second user
    data = json.dumps({"email": "sinhanawa@gmail.com", "password": hash_password("ilovecse"), "name_first": "Sinha", "name_last": "Nawa"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token = payload["token"]
    u_id2 = payload["u_id"]
    #attempting to join the channel with second user
    data = json.dumps({"token": token, "channel_id": channel_id}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/join",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #chcking that the second user was invited to the channel
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token}&channel_id={channel_id}")
    payload = json.load(response)
    assert payload == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            }
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
            {
                'u_id': u_id2,
                'name_first': 'Sinha',
                'name_last': 'Nawa',
            }
        ],
    }

def test_channel_leave():
    '''test successful leave for a user in a channel'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token1 = payload["token"]
    u_id1 = payload["u_id"]
    #create a new channel
    data = json.dumps({"token": token1, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id = payload["channel_id"]
    #create a second user
    data = json.dumps({"email": "sinhanawa@gmail.com", "password": hash_password("ilovecse"), "name_first": "Sinha", "name_last": "Nawa"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token2 = payload["token"]
    u_id2 = payload["u_id"]
    #attempting to join the channel with second user
    data = json.dumps({"token": token2, "channel_id": channel_id}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/join",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #chcking that the second user was added to the channel
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token1}&channel_id={channel_id}")
    payload = json.load(response)
    assert payload == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            }
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
            {
                'u_id': u_id2,
                'name_first': 'Sinha',
                'name_last': 'Nawa',
            }
        ],
    }
    #attempting to leave the channel with second user
    data = json.dumps({"token": token2, "channel_id": channel_id}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/leave",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #chcking that the second user has left the channel
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token1}&channel_id={channel_id}")
    payload = json.load(response)
    assert payload == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            }
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
        ],
    }

def test_channel_addowner():
    '''test successful additional owner to a channel'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token1 = payload["token"]
    u_id1 = payload["u_id"]
    #create a new channel
    data = json.dumps({"token": token1, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id = payload["channel_id"]
    #create a second user
    data = json.dumps({"email": "sinhanawa@gmail.com", "password": hash_password("ilovecse"), "name_first": "Sinha", "name_last": "Nawa"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token2 = payload["token"]
    u_id2 = payload["u_id"]
    #making the second user an owner
    data = json.dumps({"token": token1, "channel_id": channel_id, "u_id": u_id2}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/addowner",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #chcking that the second user was added to the channel as an owner
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token1}&channel_id={channel_id}")
    payload = json.load(response)
    assert payload == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
            {
                'u_id': u_id2,
                'name_first': 'Sinha',
                'name_last': 'Nawa',
            }
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
            {
                'u_id': u_id2,
                'name_first': 'Sinha',
                'name_last': 'Nawa',
            }
        ],
    }

def test_channel_removeowner():
    '''test successful removal as an owner to a member in a channel'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token1 = payload["token"]
    u_id1 = payload["u_id"]
    #create a new channel
    data = json.dumps({"token": token1, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id = payload["channel_id"]
    #create a second user
    data = json.dumps({"email": "sinhanawa@gmail.com", "password": hash_password("ilovecse"), "name_first": "Sinha", "name_last": "Nawa"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token2 = payload["token"]
    u_id2 = payload["u_id"]
    #making the second user an owner
    data = json.dumps({"token": token1, "channel_id": channel_id, "u_id": u_id2}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/addowner",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #chcking that the second user was added to the channel as an owner
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token1}&channel_id={channel_id}")
    payload = json.load(response)
    assert payload == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
            {
                'u_id': u_id2,
                'name_first': 'Sinha',
                'name_last': 'Nawa',
            }
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
            {
                'u_id': u_id2,
                'name_first': 'Sinha',
                'name_last': 'Nawa',
            }
        ],
    }
    #removing the second user as an owner
    data = json.dumps({"token": token1, "channel_id": channel_id, "u_id": u_id2}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/removeowner",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #chcking that the second user was removed as an owner
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token1}&channel_id={channel_id}")
    payload = json.load(response)
    assert payload == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
            {
                'u_id': u_id2,
                'name_first': 'Sinha',
                'name_last': 'Nawa',
            }
        ],
    }

def test_channel_messages():
    '''test successful removal as an owner to a member in a channel
    Note that this will always be off by a couple ms but everything else matches'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token = payload["token"]
    u_id = payload["u_id"]
    #create a new channel
    data = json.dumps({"token": token, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id = payload["channel_id"]
    data = json.dumps({"token": token, "channel_id": channel_id, "message": "Hello World"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    curr_time = datetime.now()
    timestamp1 = curr_time.replace(tzinfo=timezone.utc).timestamp()
    payload = json.load(response)
    message_id1 = payload["message_id"]
    data = json.dumps({"token": token, "channel_id": channel_id, "message": "Yes Please"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    curr_time = datetime.now()
    timestamp2 = curr_time.replace(tzinfo=timezone.utc).timestamp()
    payload = json.load(response)
    message_id2 = payload["message_id"]
    response = urllib.request.urlopen(f"{BASE_URL}/channel/messages?token={token}&channel_id={channel_id}&start=0")
    payload = json.load(response)
    assert payload == {
        'messages': [
            {
                'message_id': message_id2,
                'u_id': u_id,
                'message': 'Yes Please',
                'time_created': timestamp2,
            },
            {
                'message_id': message_id1,
                'u_id': u_id,
                'message': 'Hello World',
                'time_created': timestamp1,
            }
        ],
        'start': 0,
        'end': -1,
    }
    # Note that this will always be off by a couple ms but everything else matches

# --------------
# Channels Tests
# --------------

def test_channels_create():
    '''test successful creation of a channel'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token = payload["token"]
    u_id = payload["u_id"]
    #create a new channel
    data = json.dumps({"token": token, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id = payload["channel_id"]
    #chcking that the channel is listed
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token}&channel_id={channel_id}")
    payload = json.load(response)
    assert payload == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            }
        ],
        'all_members': [
            {
                'u_id': u_id,
                'name_first': 'Robbie',
                'name_last': 'Caldwell',
            },
        ],
    }

def test_channels_listall():
    '''test successful list of all channels'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token = payload["token"]
    u_id = payload["u_id"]
    #create a new channel
    data = json.dumps({"token": token, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id1 = payload["channel_id"]
    #create a second channel
    data = json.dumps({"token": token, "name": "Here We Go Again", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id2 = payload["channel_id"]
    #create a third channel
    data = json.dumps({"token": token, "name": "Another One", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id3 = payload["channel_id"]
    #chcking that the channel is listed
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)
    assert payload == {
        'channels': [
            {
                'channel_id': channel_id1,
                'name': 'New Channel',
            },
            {
                'channel_id': channel_id2,
                'name': 'Here We Go Again',
            },
            {
                'channel_id': channel_id3,
                'name': 'Another One',
            },
        ],
    }

def test_channels_list():
    '''test successful list of all channels'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token1 = payload["token"]
    u_id = payload["u_id"]
    #create a second user
    data = json.dumps({"email": "sinhanawa@gmail.com", "password": hash_password("ilovecse"), "name_first": "Sinha", "name_last": "Nawa"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token2 = payload["token"]
    #create a new channel
    data = json.dumps({"token": token1, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id1 = payload["channel_id"]
    #create a second channel
    data = json.dumps({"token": token2, "name": "Here We Go Again", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id2 = payload["channel_id"]
    #create a third channel
    data = json.dumps({"token": token1, "name": "Another One", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    channel_id3 = payload["channel_id"]
    #chcking that the channel is listed
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token1}")
    payload = json.load(response)
    assert payload == {
        'channels': [
            {
                'channel_id': channel_id1,
                'name': 'New Channel',
            },
            {
                'channel_id': channel_id3,
                'name': 'Another One',
            },
        ],
    }

# -------------
# Message Tests
# -------------

def test_send_message_later():
    '''testing for sending a message in the future'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #register for a new user
    data = json.dumps({"email": "jiaqi@gmail.com", "password": hash_password("ilovecse"), "name_first": "Jiaqi", "name_last": "Zhu"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #create a new channel
    payload = json.load(response)
    token = payload['token']
    data = json.dumps({"token": token, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #send a message later
    payload = json.load(response)
    channel_id = payload['channel_id']
    curr_time = datetime.now()
    time_stamp = curr_time.replace(tzinfo=timezone.utc).timestamp()
    data = json.dumps({"token": token, "channel_id": channel_id, "message": "Hello everyone", "time_sent": time_stamp + 5}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/message/sendlater",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    sleep(5)
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {"message_id": 1}

def test_send_message():
    '''testing for sending a message'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #register for a new user
    data = json.dumps({"email": "scnawa@hotmail.com", "password": hash_password("ilovecse"), \
        "name_first": "Sinha", "name_last": "Nawa"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #create a new channel
    payload = json.load(response)
    token = payload['token']
    data = json.dumps({"token": token, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #send a message 
    payload = json.load(response)
    channel_id = payload['channel_id']
    data = json.dumps({"token": token, "channel_id": channel_id, "message": "Hello everyone"}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {"message_id": 1}

def test_message_pin():
    '''testing message pin'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #register for a new user
    data = json.dumps({"email": "scnawa@hotmail.com", "password": hash_password("ilovecse"), \
        "name_first": "Sinha", "name_last": "Nawa"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #create a new channel
    payload = json.load(response)
    token = payload['token']
    data = json.dumps({"token": token, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #send a message 
    payload = json.load(response)
    channel_id = payload['channel_id']
    data = json.dumps({"token": token, "channel_id": channel_id, "message": "Hello everyone"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #react to a message
    payload = json.load(response)
    message_id = payload['message_id']
    data = json.dumps({"token": token, "message_id": message_id }).encode("utf-8")
    response = urllib.request.Request(
        f"{BASE_URL}/message/pin",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    )

def test_message_unpin():
    '''testing unpinning a message'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #register for a new user
    data = json.dumps({"email": "scnawa@hotmail.com", "password": hash_password("ilovecse"), \
        "name_first": "Sinha", "name_last": "Nawa"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #create a new channel
    payload = json.load(response)
    token = payload['token']
    data = json.dumps({"token": token, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #send a message
    payload = json.load(response)
    channel_id = payload['channel_id']
    data = json.dumps({"token": token, "channel_id": channel_id, "message": "Hello everyone"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #pin a message
    payload = json.load(response)
    message_id = payload['message_id']
    data = json.dumps({"token": token, "message_id": message_id}).encode("utf-8")
    response = urllib.request.Request(
        f"{BASE_URL}/message/pin",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    #unpin to a message
    data = json.dumps({"token": token, "message_id": message_id}).encode("utf-8")
    response = urllib.request.Request(
        f"{BASE_URL}/message/unpin",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    )

# -------------
# Standup Tests
# -------------

def test_standup_start():
    '''testing for standup/start'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #register for a new user
    data = json.dumps({"email": "jiaqi@gmail.com", "password": hash_password("ilovecse"), "name_first": "Jiaqi", "name_last": "Zhu"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #create a new channel
    payload = json.load(response)
    token = payload['token']
    data = json.dumps({"token": token, "name": "New Channel", "is_public": True}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #send a message later
    payload = json.load(response)
    channel_id = payload['channel_id']
    data = json.dumps({"token": token, "channel_id": channel_id, "length": 5}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/standup/start",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    start = time.time()
    with urllib.request.urlopen(req) as response:
        payload = json.load(response)
    curr_time = datetime.utcnow()
    time_stamp = curr_time.replace(tzinfo=timezone.utc).timestamp()
    time_finish = time_stamp + 5 + time.time() - start
    assert round(payload['time_finish'], 0) == round(time_finish, 0)

    response = urllib.request.urlopen(f"{BASE_URL}/standup/active?token={token}&channel_id={channel_id}")
    payload = json.load(response)
    assert payload["is_active"] is True

def test_workspace_reset():
    '''Test if workspace is cleaned after reset'''
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST')
    with urllib.request.urlopen(req) as response:
        res = json.load(response)
    assert res == {}

# ----------
# User Tests
# ----------

def test_user_profile_self():
    '''test successful check in someones own profile'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    payload = json.load(response)
    token = payload["token"]
    u_id = payload["u_id"]
    #checking the name change was successful
    response = urllib.request.urlopen(f"{BASE_URL}/user/profile?token={token}&u_id={u_id}")
    payload = json.load(response)
    assert payload == {
        "user": {
            "u_id": u_id,
            "email": "robbiecaldwell@gmail.com",
            "name_first": "Robbie",
            "name_last": "Caldwell",
            "handle_str":get_handle("Robbie", "Caldwell"),
        }
    }

def test_user_profile_setname():
    '''test successful change in profile name'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #changing the users name
    payload = json.load(response)
    token = payload["token"]
    data = json.dumps({"token": token, "name_first": "Sinha", "name_last": "Nawa"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/user/profile/setname",
        data=data,
        headers={"Content-Type": "application/json"},
        method='PUT'
    ))
    #checking the name change was successful
    response = urllib.request.urlopen(f"{BASE_URL}/users/all?token={token}")
    payload = json.load(response)
    assert payload == {
        "users": [{
            "u_id": 1,
            "email": "robbiecaldwell@gmail.com",
            "name_first": "Sinha",
            "name_last": "Nawa",
            "handle_str":get_handle("Robbie", "Caldwell"),
        }]
    }

def test_user_profile_setemail():
    '''test successful user profile check'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #changing the users email
    payload = json.load(response)
    token = payload["token"]
    data = json.dumps({"token": token, "email": "sinhanawa@gmail.com"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/user/profile/setemail",
        data=data,
        headers={"Content-Type": "application/json"},
        method='PUT'
    ))
    #chcking that the email change was successful
    response = urllib.request.urlopen(f"{BASE_URL}/users/all?token={token}")
    payload = json.load(response)
    assert payload == {
        "users": [{
            "u_id": 1,
            "email": "sinhanawa@gmail.com",
            "name_first": "Robbie",
            "name_last": "Caldwell",
            "handle_str":get_handle("Robbie", "Caldwell"),
        }]
    }

def test_user_profile_setemail_taken():
    '''test when email is already taken'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #register for a second new user
    data = json.dumps({"email": "jiaqi@gmail.com", "password": hash_password("ilovecse"), "name_first": "Jiaqi", "name_last": "Zhu"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #changing the users email
    payload = json.load(response)
    token = payload["token"]
    data = json.dumps({"token": token, "email": "robbiecaldwell@gmail.com"}).encode("utf-8")
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/user/profile/setemail",
            data=data,
            headers={"Content-Type": "application/json"},
            method='PUT'
        ))

def test_user_profile_sethandle():
    '''test successful user profile check'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #changing the users handle
    payload = json.load(response)
    token = payload["token"]
    data = json.dumps({"token": token, "handle_str": "Masters_Material"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/user/profile/sethandle",
        data=data,
        headers={"Content-Type": "application/json"},
        method='PUT'
    ))
    #chcking that the handle change was successful
    response = urllib.request.urlopen(f"{BASE_URL}/users/all?token={token}")
    payload = json.load(response)
    assert payload == {
        "users": [{
            "u_id": 1,
            "email": "robbiecaldwell@gmail.com",
            "name_first": "Robbie",
            "name_last": "Caldwell",
            "handle_str":"Masters_Material",
        }]
    }

def test_user_profile_sethandle_taken():
        '''test when handle is already taken'''
    #reset workspace
    urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST'))
    #create a new user
    data = json.dumps({"email": "robbiecaldwell@gmail.com", "password": hash_password("ilovecse"), "name_first": "Robbie", "name_last": "Caldwell"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #register for a second new user
    data = json.dumps({"email": "jiaqi@gmail.com", "password": hash_password("ilovecse"), "name_first": "Jiaqi", "name_last": "Zhu"}).encode("utf-8")
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    ))
    #changing the users handle
    payload = json.load(response)
    token = payload["token"]
    data = json.dumps({"token": token, "handle": get_handle("Robbie", "Caldwell")}).encode("utf-8")
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/user/profile/sethandle",
            data=data,
            headers={"Content-Type": "application/json"},
            method='PUT'
        ))