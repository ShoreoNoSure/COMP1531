import auth
import message
import channel
import channels
import pytest
from error import InputError

#testing message send
def test_message_send():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    channels.channels_create(token, "Test_channel", True)
    assert message.message_send(token, "1", "test") == { 'message_id': 1,}
    

#testing message send with wrong token    
def test_message_wrong_token():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    channels.channels_create(token, "Test_channel", True)
    with pytest.raises(InputError):
        message.message_send("1234567", "1", "a")

#testing message send over limit
def test_message_send_overlimit():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    with pytest.raises(InputError):
        message.message_send(token, "1", "a"*1001)

#testing message send over limit
def test_message_send_overlimit2():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    with pytest.raises(InputError):
        message.message_send(token, "1", "a"*10000)

#testing message send no permissions        
def test_message_send_no_permission():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    channels.channels_create(token, "Test_channel", False)
    channel.channel_leave(token, "1")
    with pytest.raises(AccessError):
        message.message_send(token, "1", "Test message")
