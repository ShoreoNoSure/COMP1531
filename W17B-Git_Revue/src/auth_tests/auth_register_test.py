import auth
import pytest
from error import InputError
import re
import user


#testing register funcion
def test_register():
    assert(profile['user']['u_id'] == u_id)
    assert(profile['user']['name_first'] == "Sinha")
    assert(profile['user']['name_first'] == "Nawa")
    assert(profile['user']['email'] == "scnawa@hotmail.com")
    assert auth.auth_register ("scnawa@hotmail.com", "123456", "Sinha", "Nawa") == {
        'u_id': 1,
        'token': '12345',
    }

#testing register funcion with user already registered    
def test_register_with_already_used():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    with pytest.raises(InputError):
        auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
        
#testing register funcion with wrong email        
def test_register_email_wrong():
    
    with pytest.raises(InputError):

        auth.auth_register("chinaxyzpokemon.com", "123456", "Sinha", "Nawa")

#testing register funcion with invalid password        
def test_register_password_wrong():
    
    with pytest.raises(InputError):
        auth.auth_register("scnawa@hotmail.com", "12345", "Sinha", "Nawa")

#testing register funcion with invalid first name        
def test_register_first_name_wrong():
    
    with pytest.raises(InputError):
        auth.auth_register("scnawa@hotmail.com.com", "123456", "Sinhaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "Nawa")

#testing register funcion with invalid last name  
def test_register_last_name_wrong():
    
    with pytest.raises(InputError):
        auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    
