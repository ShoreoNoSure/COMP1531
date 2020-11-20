import user
import auth

import pytest
from error import InputError


def test_invalid_email():

    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    token = login['token']

    #email does not contain the @
    with pytest.raises(InputError):
        user.user_profile_setemail(token, 'cs1531.unsw.edu.au')

def test_valid_email():

    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    token = login['token']

    profile = user.user_profile(token, u_id)
    #checking email before it is changed
    assert(profile['user']['email'] == 'cse1531@cse.unsw.edu.au')

    #checking that email has properly changed
    user.user_profile_setemail(token, 'robbiecaldwell@gmail.com')
    assert(profile['user']['email'] == 'robbiecaldwell@gmail.com')


def test_email_already_taken():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    token = login['token']
 
    profile = user.user_profile(token, u_id)
    assert(profile['user']['email'] == 'cse1531@cse.unsw.edu.au')
    auth.auth_logout(token)

    login2 = auth.auth_register("robbiecaldwell@gmail.com", "123456", 
    "Robbie", "Caldwell")

    token = login2['token']
    assert(profile['user']['email'] == 'robbiecaldwell@gmail.com')

    #attempting to change to an already taken email
    with pytest.raises(InputError):
        user.user_profile_setemail(token, 'cs1531@cse.unsw.edu.au')

    
def test_invalid_token():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    token = login['token']

    with pytest.raises(InputError):
        user.user_profile_setemail("".join((token, 'wrong')), 'robbiecaldwell@gmail.com')


def test_no_email_input():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    token = login['token']

    with pytest.raises(InputError):
        user.user_profile_setemail(token, "")