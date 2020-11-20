import auth
import pytest
from error import InputError

# Testing for an inccorect password error        
def test_incorrect_password():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    auth.auth_logout(token)
    with pytest.raises(InputError):
        auth.auth_login("scnawa@hotmail.com", "qwertyuiop")

# Testing for an inccorect password and email error    
def test_incorrect_password_and_email():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    auth.auth_logout(token)
   
    with pytest.raises(InputError):
        auth.auth_login("china@hotmail.com", "qwertyuiop")

# Testing for an corect password  
def test_correct_password():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    auth.auth_logout(token)
   
    assert auth.auth_login("scnawa@hotmail.com", "123456") == {
       'u_id': 1,
       'token': '12345',
    }

# Testing for an inccorect email error    
def test_incorrect_email():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    auth.auth_logout(token)
   
    with pytest.raises(InputError):
        auth.auth_login("china@hotmail.com", "123456")

# Testing for an inccorect email error 
def test_incorrect_email_2():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    auth.auth_logout(token)
   
    with pytest.raises(InputError):
        auth.auth_login("sncawa@hotmail.com", "123456")
        

         
# Testing for no users
def test_no_users_at_all():
    with pytest.raises(InputError):
        auth.auth_login("scnawa@hotmail.com", "123456")  

# Testing for already logged in
def test_already_logged_in():
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    assert auth.auth_login("scnawa@hotmail.com", "123456") == {
       'u_id': 1,
       'token': '12345',
    } 
    
   

    
        

