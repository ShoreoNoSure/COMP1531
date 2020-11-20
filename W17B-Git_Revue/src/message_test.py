#pylint: disable = missing-docstring
from datetime import datetime, timezone
import pytest
import message
import auth
import channel
import channels
from error import InputError, AccessError
from helper import reset_data, get_data

#------------------
#Testing message send functions
#------------------
#Testing message send
def test_message_send():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", True)
    assert message.message_send(owner['token'], 1, "test") == {'message_id': 1,}

#testing message send over limit
def test_message_send_overlimit():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", False)
    with pytest.raises(InputError):
        message.message_send(owner['token'], 1, "a"*1001)

#testing message send over limit
def test_message_send_overlimit2():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", False)
    with pytest.raises(InputError):
        message.message_send(owner['token'], 1, "a"*10000)

#testing message send no permissions
def test_message_send_no_permission():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", False)
    channel.channel_leave(owner['token'], 1)
    with pytest.raises(AccessError):
        message.message_send(owner['token'], 1, "Test message")

#------------------
#Testing message remove functions
#------------------
#Testing message remove
def test_message_remove():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", True)
    message.message_send(owner['token'], 1, "test")
    assert message.message_remove(owner['token'], 1) == {}

#testing message remove already removed
def test_message_remove_already_removed():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_remove(owner['token'], 1)
    with pytest.raises(InputError):
        message.message_remove(owner['token'], 1)

#testing message remove no message
def test_message_remove_no_messages():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", True)
    with pytest.raises(InputError):
        message.message_remove(owner['token'], 1)

#testing message remove not owner but sender
def test_message_remove_not_owner_but_sender():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", True)
    message.message_send(owner['token'], 1, "test")
    channel.channel_removeowner(owner['token'], 1, 1)
    assert message.message_remove(owner['token'], 1) == {}

#testing message remove
def test_message_remove_not_sender_but_owner():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    member = auth.auth_register("scnawa1@hotmail.com", "1234567", "Sinha1", "Nawa1")
    channels.channels_create(owner['token'], "Test_channel", True)
    channel.channel_join(member['token'], 1)
    message.message_send(member['token'], 1, "test")
    assert message.message_remove(owner['token'], 1) == {}

#testing message remove neither owner nor sender
def test_message_remove_neither_owner_nor_sender():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    member = auth.auth_register("scnawa1@hotmail.com", "1234567", "Sinha1", "Nawa1")
    channels.channels_create(owner['token'], "Test_channel", True)
    message.message_send(owner['token'], 1, "test")
    channel.channel_invite(owner['token'], 1, member['u_id'])
    channel.channel_removeowner(owner['token'], 1, 1)
    with pytest.raises(AccessError):
        message.message_remove(member['token'], 1)

#------------------
#Testing message edit functions
#------------------

#Testing message edit function
def test_message_edit():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", True)
    message.message_send(owner['token'], 1, "test")
    assert message.message_edit(owner['token'], 1, "Help") == {}

#testing message edit function
def test_message_edit2():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", True)
    message.message_send(owner['token'], 1, "test")
    assert message.message_edit(owner['token'], 1, "Second test") == {}

#testing message edit function to edit it to an empty message
def test_message_edit_empty_message():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", True)
    message.message_send(owner['token'], 1, "test")
    assert message.message_edit(owner['token'], 1, "") == \
        message.message_remove(owner['token'], 1)

#testing message edit function when not owner or sender
def test_message_edit_not_owner_or_sender():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    member = auth.auth_register("scnawa1@hotmail.com", "123456", "Sinha1", "Nawa1")
    channels.channels_create(owner['token'], "Test_channel", True)
    message.message_send(owner['token'], 1, "test")
    channel.channel_removeowner(owner['token'], 1, 1)
    with pytest.raises(AccessError):
        message.message_edit(member['token'], 1, "Wrong message id")

#testing message edit function when not sender but owner
def test_message_edit_not_sender_but_owner():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", True)
    message.message_send(owner['token'], 1, "test")
    assert message.message_edit(owner['token'], 1, "") == {}

#testing message edit function not owner but sender
def test_message_edit_not_owner_but_sender():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "Test_channel", True)
    message.message_send(owner['token'], 1, "test")
    channel.channel_removeowner(owner['token'], 1, 1)
    assert message.message_edit(owner['token'], 1, "") == {}

#------------------
#Testing message sendlater functions
#------------------
def test_sendlater():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    d_t = datetime.now()
    timestamp = d_t.replace(tzinfo=timezone.utc).timestamp()
    assert message.message_sendlater(owner['token'], 1, "Test", timestamp+1000) == \
        {'message_id': 1}

def test_invalid_channel():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    d_t = datetime.now()
    timestamp = d_t.replace(tzinfo=timezone.utc).timestamp()
    with pytest.raises(InputError):
        message.message_sendlater(owner['token'], 2, "Test", timestamp+1000)

def test_message_sendlater_overlimit():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    d_t = datetime.now()
    timestamp = d_t.replace(tzinfo=timezone.utc).timestamp()
    with pytest.raises(InputError):
        message.message_sendlater(owner['token'], 1, "a"*1001, timestamp+1000)

def test_message_sendlater_in_past():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    d_t = datetime.utcnow()
    timestamp = d_t.replace(tzinfo=timezone.utc).timestamp()
    with pytest.raises(InputError):
        message.message_sendlater(owner['token'], 1, "Past", timestamp - 1000000)

def test_message_sendlater_in_another_channel():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    member = auth.auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    channels.channels_create(owner['token'], "New Channel", True)
    d_t = datetime.now()
    timestamp = d_t.replace(tzinfo=timezone.utc).timestamp()
    with pytest.raises(AccessError):
        message.message_sendlater(member['token'], 1, "Test", timestamp+1000)

#------------------
#Testing message pin functions
#------------------
#Testing for pin
def test_pin():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_pin(owner['token'], 1)
    data = get_data()
    msg = data['messages'][0]
    assert msg['is_pinned'] == 1

#Testing for invalid ID
def test_invalid_id():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    with pytest.raises(InputError):
        message.message_pin(owner['token'], 2)

#Testing for not owner
def test_not_owner():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "hellocse1", "Sinha", "Nawa")
    member = auth.auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    channels.channels_create(owner['token'], "New Channel", True)
    channel.channel_invite(owner['token'], 1, member['u_id'])
    message.message_send(owner['token'], 1, "test")
    with pytest.raises(InputError):
        message.message_pin(member['token'], 1)

#Testing for already pinned
def test_already_pinned():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.edu.au", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_pin(owner['token'], 1)
    with pytest.raises(InputError):
        message.message_pin(owner['token'], 1)

#Testing for not in channel
def test_not_owner2():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "hellocse1", "Sinha", "Nawa")
    member = auth.auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    with pytest.raises(AccessError):
        message.message_pin(member['token'], 1)

#------------------
#Testing message unpin functions
#------------------
#Testing for unpin
def test_unpin():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "hellocse", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_pin(owner['token'], 1)
    message.message_unpin(owner['token'], 1)
    data = get_data()
    msg = data['messages'][0]
    assert msg['is_pinned'] is False

#Testing for invalid ID
def test_invalid_id1():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_pin(owner['token'], 1)
    with pytest.raises(InputError):
        message.message_unpin(owner['token'], 2)

#Testing for not owner
def test_not_owner1():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "hellocse1", "Sinha", "Nawa")
    member = auth.auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    channels.channels_create(owner['token'], "New Channel", True)
    channel.channel_invite(owner['token'], 1, member['u_id'])
    message.message_send(owner['token'], 1, "test")
    message.message_pin(owner['token'], 1)
    with pytest.raises(InputError):
        message.message_unpin(member['token'], 1)

#Testing for already unpinned
def test_already_unpinned():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_pin(owner['token'], 1)
    message.message_unpin(owner['token'], 1)
    with pytest.raises(InputError):
        message.message_unpin(owner['token'], 1)

#Testing for not in channel
def test_not_owner3():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.edu.au", "hellocse1", "Sinha", "Nawa")
    member = auth.auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_pin(owner['token'], 1)
    with pytest.raises(AccessError):
        message.message_unpin(member['token'], 1)
#------------------
#Testing message react functions
#------------------
#Testing react
def test_react():
    reset_data()
    owner = auth.auth_register("scnaw@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_react(owner['token'], 1, 1)
    data = get_data()
    msg = data['messages'][0]
    assert msg['react'] == [{'react_id': 1, 'u_id': 1}]

#Testing another user react
def test_another_react():
    reset_data()
    owner = auth.auth_register("scnaw@hotmail.com", "hellocse1", "Sinha", "Nawa")
    member = auth.auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    channels.channels_create(owner['token'], "New Channel", True)
    channel.channel_invite(owner['token'], 1, member['u_id'])
    message.message_send(owner['token'], 1, "test")
    message.message_react(member['token'], 1, 1)
    data = get_data()
    msg = data['messages'][0]
    assert msg['react'] == [{'react_id': 1, 'u_id': 2}]

#Testing another user react
def test_multiple_reacts():
    reset_data()
    owner = auth.auth_register("scnaw@hotmail.com", "hellocse1", "Sinha", "Nawa")
    member = auth.auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    channels.channels_create(owner['token'], "New Channel", True)
    channel.channel_invite(owner['token'], 1, member['u_id'])
    message.message_send(owner['token'], 1, "test")
    message.message_react(owner['token'], 1, 1)
    message.message_react(member['token'], 1, 1)
    data = get_data()
    msg = data['messages'][0]
    assert msg['react'] == [{'react_id': 1, 'u_id': 1}, {'react_id': 1, 'u_id': 2}]

#Testing not in channel
def test_not_in_channel():
    reset_data()
    owner = auth.auth_register("scnaw@hotmail.com", "hellocse1", "Sinha", "Nawa")
    member = auth.auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    with pytest.raises(InputError):
        message.message_react(member['token'], 1, 1)

#Testinginvalid react_id
def test_invalid_react_id():
    reset_data()
    owner = auth.auth_register("scnaw@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    with pytest.raises(InputError):
        message.message_react(owner['token'], 1, 2)

#Testing react already react
def test_react_again():
    reset_data()
    owner = auth.auth_register("scnaw@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_react(owner['token'], 1, 1)
    with pytest.raises(InputError):
        message.message_react(owner['token'], 1, 1)

#------------------
#Testing message unreact functions
#------------------
#Testing unreact
def test_unreact():
    reset_data()
    owner = auth.auth_register("scnaw@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_react(owner['token'], 1, 1)
    message.message_unreact(owner['token'], 1, 1)
    data = get_data()
    msg = data['messages'][0]
    assert msg['react'] == []

#Testing another user unreact
def test_another_unreact():
    reset_data()
    owner = auth.auth_register("scnaw@hotmail.com", "hellocse1", "Sinha", "Nawa")
    member = auth.auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    channels.channels_create(owner['token'], "New Channel", True)
    channel.channel_invite(owner['token'], 1, member['u_id'])
    message.message_send(owner['token'], 1, "test")
    message.message_react(member['token'], 1, 1)
    message.message_unreact(member['token'], 1, 1)
    data = get_data()
    msg = data['messages'][0]
    assert msg['react'] == []

#Testing not in channel
def test_not_in_channel1():
    reset_data()
    owner = auth.auth_register("scnaw@hotmail.com", "hellocse1", "Sinha", "Nawa")
    member = auth.auth_register("jiaqi@unsw.edu.au", "hellocse", "jiaqi", "zhu")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    with pytest.raises(InputError):
        message.message_unreact(member['token'], 1, 1)

#Testing not invalid unreact_id
def test_invalid_unreact_id():
    reset_data()
    owner = auth.auth_register("scnaw@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_react(owner['token'], 1, 1)
    with pytest.raises(InputError):
        message.message_unreact(owner['token'], 1, 2)

#Testing unreact to an unreacted message
def test_unreacted_msg():
    reset_data()
    owner = auth.auth_register("scnaw@hotmail.com", "hellocse1", "Sinha", "Nawa")
    channels.channels_create(owner['token'], "New Channel", True)
    message.message_send(owner['token'], 1, "test")
    message.message_react(owner['token'], 1, 1)
    message.message_unreact(owner['token'], 1, 1)
    with pytest.raises(InputError):
        message.message_unreact(owner['token'], 1, 1)
