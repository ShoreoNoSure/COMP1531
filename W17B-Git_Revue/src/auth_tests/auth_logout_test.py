import auth
import pytest

        
#Testing logout        
def test_logout():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    assert auth.auth_logout(token) ==  {
        'is_success': True,
    }

#Testing logout fails
def test_logout_false():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    assert auth.auth_logout(token) ==  {
        'is_success': False,
    }

#Testing logout when not logged in
def test_logout_when_not_logged_in():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    auth.auth_logout(token)
    assert auth.auth_logout(token) ==  {
        'is_success': False,
    }

#Testing logout with login multiple times      
def test_logout_login():
    # if check(email) == True
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]       
    auth.auth_logout("12345")
    auth.auth_login("scnawa@hotmail.com", "123456")
    assert auth.auth_logout(token) ==  {
        'is_success': True,
    }
    
