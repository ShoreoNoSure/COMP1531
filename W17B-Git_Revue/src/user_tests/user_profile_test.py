'''import modules'''
import pytest
import user
import auth
from error import InputError

def test_profile_success():
    '''test for success case'''
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", "Hayden", "Jacobs")
    auth.auth_login("cs1531@cse.unsw.edu.au", "123456")
    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")
    profile = user.user_profile(token, u_id)
    assert profile['user'] == {
        'u_id': u_id,
        'email': "cs1531@cse.unsw.edu.au",
        'name_first': "Hayden",
        'name_last': "Jacobs",
        'handle_str': "hjacobs"
    }

def test_profile_fail():
    '''test for failed case'''
    login = auth.auth_register("robbiecaldwell@gmail.com", "123456", "robbie", "caldwell")
    auth.auth_login("robbiecadlwell@gmail.com", "123456")
    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "Robbae01")
    with pytest.raises(InputError):
        user.user_profile(token, u_id + 1)
    #since there is only one profile to check, adding 1 to the u_id will create a unique u_id.
