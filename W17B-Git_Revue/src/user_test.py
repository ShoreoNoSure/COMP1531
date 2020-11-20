#pylint: disable = missing-docstring
import pytest
import auth
import user
from helper import reset_data
from error import InputError, AccessError

# ------------------------
# Testing for user_profile
# ------------------------

# Test that user_profile returns a dictionary with all the users info
def test_profile_success():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")
    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    assert user.user_profile(token, u_id) == {
        'user': {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'hjacobs'
        }
    }

# Test input error for an invalid u_id
def test_profile_fail():
    reset_data()
    login = auth.auth_register("robbiecaldwell@gmail.com", "123456", "robbie", "caldwell")
    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "Robbae01")

    with pytest.raises(InputError):
        user.user_profile(token, u_id + 1)
    #since there is only one profile to check, adding 1 to the u_id will create a unique u_id.

# Test checking someone elses profile
def test_profile_check_else():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")
    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")
    auth.auth_logout(token)
    login = auth.auth_register("robbiecaldwell@gmail.com", "123456", "robbie", "caldwell")
    token = login['token']

    assert user.user_profile(token, u_id) == {
        'user': {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'hjacobs',
        }
    }

# Test with invalid token
def test_token_incorrect():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")
    token = login['token']

    with pytest.raises(AccessError):
        user.user_profile("".join((token, 'wrong')), "u_id")

# --------------------------------
# Testing for user_profile_setname
# --------------------------------

# Test input error raised if first name is too short
def test_name_first_too_short():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    auth.auth_login("cs1531@cse.unsw.edu.au", "123456")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    user.user_profile(token, u_id)
    with pytest.raises(InputError):
        user.user_profile_setname(token, "", "Jacobs")

# Test input error raised if first name is too long
def test_name_first_too_long():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    user.user_profile(token, u_id)
    with pytest.raises(InputError):
        user.user_profile_setname(token, "a"*51, "Jacobs")

# Test input error raised if last name is too short
def test_name_last_too_short():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    user.user_profile(token, u_id)
    with pytest.raises(InputError):
        user.user_profile_setname(token, "Hayden", "")

# Test input error raised if last name is too long
def test_name_last_too_long():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    user.user_profile(token, u_id)
    with pytest.raises(InputError):
        user.user_profile_setname(token, "Hayden", "a"*51)

# Test a successful change for first name
def test_name_first_success():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    user.user_profile_setname(token, "Robbie", "Jacobs") #only changes first name
    profile = user.user_profile(token, u_id)

    assert profile['user'] == {
        'u_id': 1,
        'email': 'cs1531@cse.unsw.edu.au',
        'name_first': 'Robbie',
        'name_last': 'Jacobs',
        'handle_str': 'hjacobs'
    }

# Test a successful change for second name
def test_name_last_success():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")
    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    user.user_profile_setname(token, "Hayden", "Caldwell") #only changes last name
    profile = user.user_profile(token, u_id)
    assert profile['user'] == {
        'u_id': 1,
        'email': 'cs1531@cse.unsw.edu.au',
        'name_first': 'Hayden',
        'name_last': 'Caldwell',
        'handle_str': 'hjacobs'
    }

# Test a successful change in both first and last names
def test_name_full_success():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")
    user.user_profile_setname(token, "Robbie", "Caldwell") #changes both names
    profile = user.user_profile(token, u_id)
    assert profile['user'] == {
        'u_id': 1,
        'email': 'cs1531@cse.unsw.edu.au',
        'name_first': 'Robbie',
        'name_last': 'Caldwell',
        'handle_str': 'hjacobs'
    }

# Test with invalid token
def test_token_invalid():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    user.user_profile_sethandle(token, "hjacobs")

    with pytest.raises(AccessError):
        user.user_profile_setname("".join((token, 'wrong')), "Robbie", "Caldwell")

# ---------------------------------
# Testing for user_profile_setemail
# ---------------------------------

# Test when the input email is invalid
def test_invalid_email():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")
    token = login['token']

    #email does not contain the @
    with pytest.raises(InputError):
        user.user_profile_setemail(token, 'cs1531.unsw.edu.au')

# Test a successful change in email
def test_valid_email():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    u_id = login['u_id']

    #checking that email has properly changed
    user.user_profile_setemail(token, 'robbiecaldwell@gmail.com')
    profile = user.user_profile(token, u_id)
    assert profile['user']['email'] == 'robbiecaldwell@gmail.com'

# Test when an email has been taken by another user
def test_email_already_taken():
    reset_data()
    auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")
    login2 = auth.auth_register("robbiecaldwell@gmail.com", "123456", "Robbie", "Caldwell")

    token = login2['token']
    #attempting to change to an already taken email
    with pytest.raises(InputError):
        user.user_profile_setemail(token, 'cs1531@cse.unsw.edu.au')

# Test with invalid token
def test_invalid_token():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']

    with pytest.raises(AccessError):
        user.user_profile_setemail("".join((token, 'wrong')), 'robbiecaldwell@gmail.com')

# Test with no email input at all
def test_no_email_input():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']

    with pytest.raises(InputError):
        user.user_profile_setemail(token, "")

# ----------------------------------
# Testing for user_profile_sethandle
# ----------------------------------

# Test a successful handle change
def test_sethandle_success():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")
    profile = user.user_profile(token, u_id)
    assert profile['user']['handle_str'] == 'hjacobs'

# Test that handle can be changed multiple times
def test_sethandle_change():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")
    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")
    user.user_profile_sethandle(token, 'haydenj')
    profile = user.user_profile(token, u_id)
    assert profile['user']['handle_str'] == 'haydenj'

# Test that input error is raised when handle is too short
def test_sethandle_too_short():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "h")

# Test that input error is raised when handle is too long
def test_sethandle_too_long():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "h"*21)

# Test when handle is taken by another user
def test_sethandle_already_taken():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    user.user_profile_sethandle(token, "hjacobs")

    auth.auth_logout(token)

    login2 = auth.auth_register("robbiecaldwell@gmail.com", "123456", "Robbie", "Caldwell")

    token = login2['token']
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "hjacobs")

# Test when no handle was input at all
def test_sethandle_empty():
    reset_data()
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    token = login['token']
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "")

# Test with an invalid token
def test_sethandle_invalid_token():
    reset_data()
    auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")

    with pytest.raises(AccessError):
        user.user_profile_sethandle(7830, "hjacobs")
