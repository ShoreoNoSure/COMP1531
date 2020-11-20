import auth
import message
import channel
import channels
import pytest
from error import InputError

#testing message remove
def test_message_remove():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create("12345", "Test_channel", True)
    message.message_send("12345", "1", "test") == { 'message_id': 1,}
    assert message.message_remove("12345", "1") == {}

#testing message remove already removed    
def test_message_remove_already_removed():
     dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create("12345", "Test_channel", True)
    message.message_send("12345", "1", "test") = { 'message_id': 1,}
    message.message_remove("12345", "1") = {}
    with pytest.raises(InputError):
        message.message_remove("12345", "1")

#testing message remove no message
def test_message_remove_no_messages():
     dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create("12345", "Test_channel", True)
    with pytest.raises(InputError):
        message.message_remove("12345", "1")

#testing message remove not owner but sender    
def test_message_remove_not_owner_but_sender(): 
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create("12345", "Test_channel", True)
    message.message_send("12345", "1", "test") = {'message_id': 1,}
    channel.channel_removeowner("12345", "1", "1")
    assert message.message_remove("12345", "1") == {}

#testing message remove    
def test_message_remove_not_sender_but_owner(): 
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    dict = auth.auth_register("scnawa1@hotmail.com", "1234567", "Sinha1", "Nawa1")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create("12345", "Test_channel", True)
    message.message_send("12345", "2", "test") = {'message_id': 1,}
    
    assert message.message_remove("12345", "1") == {}
    
#testing message remove neither owner nor sender    
def test_message_remove_neither_owner_nor_sender(): 
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    dict = auth.auth_register("scnawa1@hotmail.com", "1234567", "Sinha1", "Nawa1")
    token = dict["token"]
    u_id = dict["u_id"]
    channels.channels_create("12345", "Test_channel", True)
    
    message.message_send("12345", "2", "test") = {'message_id': 1,}
    channel.channel_removeowner("12345", "1", "1")
    
    with pytest.raises(AccessError);
        message.message_remove("12345", "1") 

