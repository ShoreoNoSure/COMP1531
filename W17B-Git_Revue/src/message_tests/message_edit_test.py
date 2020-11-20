import auth
import message
import channel
import channels
import pytest
from error import InputError

#testing message edit function
def test_message_edit():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create(token, "Test_channel", True)
    message.message_send(token, "1", "test") == { 'message_id': 1,}
    assert message.message_edit(token, "1", "Help") == {}

#testing message edit function
def test_message_edit2():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create(token, "Test_channel", True)
    message.message_send(token, "1", "test") == { 'message_id': 1,}
    assert message.message_edit(token, "1", "Second test") == {}

#testing message edit function to edit it to an empty message
def test_message_edit_empty_message():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create(token, "Test_channel", True)
    message.message_send(token, "1", "test") == { 'message_id': 1,}
    
    assert message.message_edit(token,, "1", "") == message.message_remove(token,, "1")


#testing message edit function when not owner or sender
def test_message_edit_not_owner_or_sender():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create(token, "Test_channel", True)
    message.message_send(token, "1", "test") == { 'message_id': 1,}
    channel.channel_removeowner(token, "1", "1")
    with pytest.raises(AccessError)
        message.message_edit(token, "2", "Wrong message id")

#testing message edit function when not sender but owner        
def test_message_edit_not_sender_but_owner():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create(token, "Test_channel", True)
    message.message_send(token, "2", "test") == { 'message_id': 1,}
    
    assert message.message_edit(token, "1", "Owner") == {}
        
        
#testing message edit function not owner but sender       
def test_message_edit_not_owner_but_sender():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create(token, "Test_channel", True)
    message.message_send(token, "1", "test") == { 'message_id': 1,}
    channel.channel_removeowner(token, "1", "1")
    assert message.message_edit(token, "1", "Sender") == {}
