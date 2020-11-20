#pylint: disable = missing-docstring
import pytest
import auth
from error import InputError, AccessError
from helper import reset_data, generate_token
#----------
#Auth login tests
#----------
# Testing for an inccorect password error
def test_incorrect_password():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    auth.auth_logout(owner['token'])
    with pytest.raises(InputError):
        auth.auth_login("scnawa@hotmail.com", "qwertyuiop")

# Testing for an inccorect password and email error
def test_incorrect_password_and_email():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    auth.auth_logout(owner['token'])
    with pytest.raises(InputError):
        auth.auth_login("china@hotmail.com", "qwertyuiop")

# Testing for an inccorect email error
def test_incorrect_email():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    auth.auth_logout(owner['token'])
    with pytest.raises(InputError):
        auth.auth_login("china@hotmail.com", "123456")

# Testing for an inccorect email error
def test_incorrect_email_2():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    auth.auth_logout(owner['token'])
    with pytest.raises(InputError):
        auth.auth_login("sncawa@hotmail.com", "123456")

# Testing for no users
def test_no_users_at_all():
    reset_data()
    with pytest.raises(InputError):
        auth.auth_login("scnawa@hotmail.com", "123456")

#----------
#Auth logout tests
#----------
#Testing logout
def test_logout():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    assert auth.auth_logout(owner['token']) == {
        'is_success': True,
    }

#Testing logout when not logged in
def test_logout_when_not_logged_in():
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    auth.auth_logout(owner['token'])
    with pytest.raises(AccessError):
        auth.auth_logout(owner['token'])

#Testing logout with login multiple times
def test_logout_login():
    # if check(email) == True
    reset_data()
    owner = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    auth.auth_logout(owner['token'])
    auth.auth_login("scnawa@hotmail.com", "123456")
    assert auth.auth_logout(owner['token']) == {
        'is_success': True,
    }
#----------
#Auth register tests
#----------
#testing register funcion
def test_register():
    reset_data()
    assert auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa") == {
        'token': generate_token(1),
        'u_id': 1
    }

#testing register funcion with user already registered
def test_register_with_already_used():
    reset_data()
    auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    with pytest.raises(InputError):
        auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")

#testing register funcion with wrong email
def test_register_email_wrong():
    reset_data()
    with pytest.raises(InputError):
        auth.auth_register("chinaxyzpokemon.com", "123456", "Sinha", "Nawa")

#testing register funcion with invalid password
def test_register_password_wrong():
    reset_data()
    with pytest.raises(InputError):
        auth.auth_register("scnawa@hotmail.com", "12345", "Sinha", "Nawa")

#testing register funcion with invalid first name
def test_register_first_name_wrong():
    reset_data()
    with pytest.raises(InputError):
        auth.auth_register("scnawa@hotmail.com.com", "123456", \
            "Sinhaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "Nawa")

#testing register funcion with invalid last name
def test_register_last_name_wrong():
    reset_data()
    with pytest.raises(InputError):
        auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", 
            "Nawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    
    
