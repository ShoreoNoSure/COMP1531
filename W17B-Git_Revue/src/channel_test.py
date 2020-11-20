'''Import modules'''
import pytest
import channel
import channels
from auth import auth_register
#from message import message_send
from error import InputError, AccessError
from helper import reset_data, get_data
from message import message_send

# ---------------------------
# Testing for channel_details
# ---------------------------

def test_show_details_owner():
    '''test for success case'''
    reset_data()
    owner = auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    test_channel = channels.channels_create(owner['token'], "New Channel", True)
    channel_id = test_channel['channel_id']
    assert channel.channel_details(owner['token'], channel_id) == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': owner['u_id'],
                'name_first': 'jiaqi',
                'name_last': 'zhu',
            }
        ],
        'all_members': [
            {
                'u_id': owner['u_id'],
                'name_first': 'jiaqi',
                'name_last': 'zhu',
            }
        ],
    }

def test_show_details_member():
    '''test for member access'''
    reset_data()
    owner = auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    member = auth_register("robbie@gmail.com", "iamrobert", "Robert", "Cad")
    member2 = auth_register("sinha@gmail.com", "happycse", 'Sinha', "Sc")
    test_channel = channels.channels_create(owner['token'], "New Channel", True)
    channel_id = test_channel['channel_id']
    channel.channel_join(member['token'], channel_id)
    channel.channel_join(member2['token'], channel_id)

    assert channel.channel_details(member['token'], channel_id) == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': owner['u_id'],
                'name_first': 'jiaqi',
                'name_last': 'zhu',
            }
        ],
        'all_members': [
            {
                'u_id': owner['u_id'],
                'name_first': 'jiaqi',
                'name_last': 'zhu',
            }, {
                'u_id': member['u_id'],
                'name_first': 'Robert',
                'name_last': 'Cad',
            }, {
                'u_id': member2['u_id'],
                'name_first': 'Sinha',
                'name_last': 'Sc',
            }
        ]
    }

def test_more_owners():
    '''add more owners and show details'''
    reset_data()
    owner = auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    test_channel = channels.channels_create(owner['token'], "New Channel", True)
    channel_id = test_channel['channel_id']
    member1 = auth_register("robbie@gmail.com", "iamrobert", "Robert", "Cad")
    member2 = auth_register("sinha@hotmail.com", "iamnotsinha", "sinha", "N")
    member3 = auth_register("sample@gmail.com", "thisissample", "first", "last")
    channel.channel_join(member1['token'], channel_id)
    channel.channel_join(member2['token'], channel_id)
    channel.channel_join(member3['token'], channel_id)
    channel.channel_addowner(owner['token'], channel_id, member2['u_id'])

    assert channel.channel_details(owner['token'], channel_id) == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': owner['u_id'],
                'name_first': 'jiaqi',
                'name_last': 'zhu',
            }, {
                'u_id': member2['u_id'],
                'name_first': 'sinha',
                'name_last': 'N',
            }
        ],
        'all_members': [
            {
                'u_id': owner['u_id'],
                'name_first': 'jiaqi',
                'name_last': 'zhu',
            }, {
                'u_id': member1['u_id'],
                'name_first': 'Robert',
                'name_last': 'Cad',
            }, {
                'u_id': member2['u_id'],
                'name_first': 'sinha',
                'name_last': 'N',
            }, {
                'u_id': member3['u_id'],
                'name_first': 'first',
                'name_last': 'last',
            }
        ]
    }

def test_invalid_channel():
    '''test for invalid channel id'''
    reset_data()
    owner = auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    with pytest.raises(InputError):
        channel.channel_details(owner['token'], 7383)

def test_not_member_of_channel():
    '''test for access error'''
    reset_data()
    owner = auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    user = auth_register("robbie@gmail.com", "iamrobert", "Robert", "Cad")
    test_channel = channels.channels_create(owner['token'], "New Channel", True)
    with pytest.raises(AccessError):
        channel.channel_details(user['token'], test_channel['channel_id'])

# --------------------------
# Testing for channel_invite
# ---------------------------

def test_success_invite_simple():
    '''tese for success case'''
    reset_data()
    user = auth_register("example@gmail.com", "helloworld", "luc", "zhou")
    owner = auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    test_channel = channels.channels_create(owner['token'], "New Channel", True)
    assert channel.channel_invite(owner['token'], test_channel['channel_id'], user['u_id']) == {
    }

def test_invalid_channel_id():
    '''test for invalid channel id'''
    reset_data()
    owner = auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    user = auth_register("cockatoo@gmail.com", "helloworld", "luc", "zhou")
    channels.channels_create(owner['token'], "New Channel", True)

    with pytest.raises(InputError):
        channel.channel_invite(owner['token'], 7498, user['u_id'])

def test_invalid_u_id():
    '''test for invalid u id'''
    reset_data()
    owner = auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    test_channel = channels.channels_create(owner['token'], "New Channel", True)
    with pytest.raises(InputError):
        channel.channel_invite(owner['token'], test_channel['channel_id'], -8)

def test_authorised_person_not_in_channel():
    '''test for access error'''
    reset_data()
    user1 = auth_register("cockatoo@gmail.com", "helloworld", "luc", "zhou")
    user2 = auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    user3 = auth_register("sample@gmail.com", "thisissample", "first", "last")

    test_channel = channels.channels_create(user2['token'], "New Channel", True)

    with pytest.raises(AccessError):
        channel.channel_invite(user1['token'], test_channel['channel_id'], user3['u_id'])

# ------------------------
# Testing for channel_join
# ------------------------

def test_success_join():
    '''test for success join'''
    reset_data()
    member = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    test_channel = channels.channels_create(owner['token'], "Basement", True)
    channel_id = test_channel['channel_id']

    assert channel.channel_join(member['token'], channel_id) == {
    }

def test_invalid_channel_id_join():
    '''test for invalid channel id'''
    reset_data()
    member = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")

    with pytest.raises(InputError):
        channel.channel_join(member['token'], 839)

def test_private_channel():
    '''test for private channel'''
    reset_data()
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    test_channel = channels.channels_create(owner['token'], "Basement", False)
    channel_id = test_channel['channel_id']
    member = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")

    with pytest.raises(AccessError):
        channel.channel_join(member['token'], channel_id)

# -------------------------
# Testing for channel.channel_leave
# -------------------------

def test_success_leave():
    '''test for success case'''
    reset_data()
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    member = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")
    test_channel = channels.channels_create(owner['token'], "Basement", True)
    channel_id = test_channel['channel_id']
    channel.channel_invite(owner['token'], channel_id, member['u_id'])

    assert channel.channel_leave(member['token'], channel_id) == {
    }

def test_invalid_channel_id_leave():
    '''for invalid channel id'''
    reset_data()
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    channels.channels_create(owner['token'], "Basement", True)

    with pytest.raises(InputError):
        channel.channel_leave(owner['token'], 839)

def test_member_not_in_channel():
    '''test for access error'''
    reset_data()
    member = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    test_channel = channels.channels_create(owner['token'], "Basement", True)
    channel_id = test_channel['channel_id']

    with pytest.raises(AccessError):
        channel.channel_leave(member['token'], channel_id)

# ----------------------------
# Testing for channel_addowner
# ----------------------------

def test_success_addowner():
    '''test for success case'''
    reset_data()
    owner = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")
    test_channel = channels.channels_create(owner['token'], "TTress", True)
    channel_id = test_channel['channel_id']
    new_owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")

    assert channel.channel_addowner(owner['token'], channel_id, new_owner['u_id']) == {
    }

def test_invalid_channel_id_add_owner():
    '''test for invalid channel id'''
    reset_data()
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    channels.channels_create(owner['token'], "Basement", True)
    member = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")

    with pytest.raises(InputError):
        channel.channel_addowner(owner['token'], 839, member['u_id'])

def test_already_owner():
    '''test for user is already an owner of channel'''
    reset_data()
    owner = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")
    test_channel = channels.channels_create(owner['token'], "TTress", True)
    channel_id = test_channel['channel_id']
    new_owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    channel.channel_addowner(owner['token'], channel_id, new_owner['u_id'])

    with pytest.raises(InputError):
        channel.channel_addowner(owner['token'], channel_id, new_owner['u_id'])

# ----------------------------
# Testing for channel_messages
# ----------------------------

def test_success_get_messages():
    '''test for success'''
    reset_data()
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    test_channel = channels.channels_create(owner['token'], "Basement", True)
    u_id = owner['u_id']
    channel_id = test_channel['channel_id']
    message_1 = message_send(owner['token'], channel_id, "Hello World")
    message_2 = message_send(owner['token'], channel_id, "Yes Please")
    data = get_data()
    time1 = data['messages'][message_1['message_id'] - 1]['time_created']
    time2 = data['messages'][message_2['message_id'] - 1]['time_created']
    assert channel.channel_messages(owner['token'], channel_id, 0) == {
        'messages': [
            {
                'message_id': message_2['message_id'],
                'u_id': u_id,
                'message': 'Yes Please',
                'time_created': time1
            },
            {
                'message_id': message_1['message_id'],
                'u_id': u_id,
                'message': 'Hello World',
                'time_created': time2
            }
        ],
        'start': 0,
        'end': -1,
    }

def test_invalid_channel_id_messages():
    '''test for invalid channel id'''
    reset_data()
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")

    with pytest.raises(InputError):
        channel.channel_messages(owner['token'], 8333, 0)

def test_exceed_total():
    '''test for start greater than total number of messages'''
    reset_data()
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    test_channel = channels.channels_create(owner['token'], "Basement", True)
    channel_id = test_channel['channel_id']
    message_send(owner['token'], channel_id, "Hello World")
    message_send(owner['token'], channel_id, "Yes Please")

    user = auth_register("jiaqi@hotmail.com", "Thisisfun", "Jiaqi", "Zhu")
    channel.channel_join(user['token'], channel_id)
    message_send(user['token'], channel_id, "Hello guys")
    message_send(user['token'], channel_id, "This is fun")

    with pytest.raises(InputError):
        channel.channel_messages(user['token'], channel_id, 7)

# -------------------------------
# Testing for channel_removeowner
# -------------------------------

def test_success_removeowner():
    '''test for success'''
    reset_data()
    owner = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")
    test_channel = channels.channels_create(owner['token'], "TTress", True)
    channel_id = test_channel['channel_id']

    new_owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    channel.channel_addowner(owner['token'], channel_id, new_owner['u_id'])

    assert channel.channel_removeowner(owner['token'], channel_id, new_owner['u_id']) == {
    }

def test_invalid_channel_id_remove_owner():
    '''test for invalid channel_id'''
    reset_data()
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    test_channel = channels.channels_create(owner['token'], "Basement", True)
    channel_id = test_channel['channel_id']
    member = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")
    channel.channel_join(member['token'], channel_id)

    with pytest.raises(InputError):
        channel.channel_removeowner(owner['token'], 839, member['u_id'])

def test_not_owner():
    '''test for user is not an owner of channel'''
    reset_data()
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    test_channel = channels.channels_create(owner['token'], "Basement", True)
    channel_id = test_channel['channel_id']
    member = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")
    channel.channel_join(member['token'], channel_id)

    with pytest.raises(InputError):
        channel.channel_removeowner(owner['token'], channel_id, member['u_id'])

#The authorised user is not an owner of the slackr or an owner of this channel.
def test_access_error():
    '''test for access error'''
    reset_data()
    owner = auth_register("blackwidow@gmail.com", "avengers", "Natasha", "Romanova")
    test_channel = channels.channels_create(owner['token'], "Basement", True)
    channel_id = test_channel['channel_id']
    member1 = auth_register("cockatoo@gmail.com", "helloworld", "Cool", "Man")
    member2 = auth_register("robbie@unsw.edu.au", "iamrobert222", "Robert", "Caldwell")
    channel.channel_join(member1['token'], channel_id)
    channel.channel_join(member2['token'], channel_id)
    channel.channel_addowner(owner['token'], channel_id, member1['u_id'])
    print("hi")

    with pytest.raises(AccessError):
        channel.channel_removeowner(member2['token'], channel_id, member1['u_id'])
