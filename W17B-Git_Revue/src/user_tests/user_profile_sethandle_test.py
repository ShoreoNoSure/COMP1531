import user
import auth

import pytest
from error import InputError

def test_sethandle_success():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
        "Hayden", "Jacobs")

    token = login['token']
    user.user_profile_sethandle(token, "hjacobs")

    profile = user.user_profile(token, u_id)
    assert(profile['user']['handle_str'] == 'hjacobs')


def test_sethandle_change():

    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
        "Hayden", "Jacobs")

    token = login['token']
    user.user_profile_sethandle(token, "hjacobs")

    profile = user.user_profile(token, u_id)
    assert(profile['user']['handle_str'] == 'hjacobs')

    user.user_profile_sethandle(token, 'haydenj')
    assert(profile['user']['handle_str'] == 'haydenj')


def test_sethandle_too_short():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
        "Hayden", "Jacobs")

    token = login['token']
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "hj")


def test_sethandle_too_long():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
        "Hayden", "Jacobs")

    token = login['token']
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "h"*21)


def test_sethandle_already_taken():

    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
        "Hayden", "Jacobs")

    token = login['token']
    user.user_profile_sethandle(token, "hjacobs")

    auth.auth_logout(token)

    login2 = auth.auth_register("robbiecaldwell@gmail.com", "123456", 
        "Robbie", "Caldwell")

    token = login2['token']
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "hjacobs")


def test_sethandle_empty():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
        "Hayden", "Jacobs")

    token = login['token']
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "")


def test_sethandle_invalid_token():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
        "Hayden", "Jacobs")

    token = login['token']
    with pytest.raises(InputError):
        user.user_profile_sethandle(token+1, "hjacobs")