import user
import auth

import pytest
from error import InputError


def test_name_first_too_short():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    auth.auth_login("cs1531@cse.unsw.edu.au", "123456")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    profile = user.user_profile(token, u_id)
    with pytest.raises(InputError):
        user.user_profile_setname(token, "", "Jacobs")
    
    
def test_name_first_too_long():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    auth.auth_login("cs1531@cse.unsw.edu.au", "123456")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    profile = user.user_profile(token, u_id)
    with pytest.raises(InputError):
        user.user_profile_setname(token, "a"*51, "Jacobs")
        
def test_name_last_too_short():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    auth.auth_login("cs1531@cse.unsw.edu.au", "123456")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    profile = user.user_profile(token, u_id)
    with pytest.raises(InputError):
        user.user_profile_setname(token, "Hayden", "")
    
    
def test_name_last_too_long():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    auth.auth_login("cs1531@cse.unsw.edu.au", "123456")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    profile = user.user_profile(token, u_id)
    with pytest.raises(InputError):
        user.user_profile_setname(token, "Hayden", "a"*51)
        

def test_name_first_success():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    auth.auth_login("cs1531@cse.unsw.edu.au", "123456")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    profile = user.user_profile(token, u_id)
    #First checking that all this information is initially correct
    assert(profile['user']['name_first'] == 'Hayden')
    assert(profile['user']['name_last'] == 'Jacobs')
    assert(profile['user']['handle_str'] == 'hjacobs')
    #changing name
    user.user_profile_setname(token, "Robbie", "Jacobs") #only changes first name
    assert(profile['user']['name_first'] == 'Robbie')
    assert(profile['user']['name_last'] == 'Jacobs')
    assert(profile['user']['handle_str'] == 'hjacobs') #shows that it is the same profile


def test_name_last_success():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    auth.auth_login("cs1531@cse.unsw.edu.au", "123456")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    profile = user.user_profile(token, u_id)
    #First checking that all this information is initially correct
    assert(profile['user']['name_first'] == 'Hayden')
    assert(profile['user']['name_last'] == 'Jacobs')
    assert(profile['user']['handle_str'] == 'hjacobs')
    #changing name
    user.user_profile_setname(token, "Hayden", "Caldwell") #only changes last name
    profile = user.user_profile(token, u_id)
    assert(profile['user']['name_first'] == 'Hayden')
    assert(profile['user']['name_last'] == 'Caldwell')
    assert(profile['user']['handle_str'] == 'hjacobs') #shows that it is the same profile


def test_name_full_success():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    auth.auth_login("cs1531@cse.unsw.edu.au", "123456")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    profile = user.user_profile(token, u_id)
    #First checking that all this information is initially correct
    assert(profile['user']['name_first'] == 'Hayden')
    assert(profile['user']['name_last'] == 'Jacobs')
    assert(profile['user']['handle_str'] == 'hjacobs')
    #changing name
    profile = user.user_profile(token, u_id)
    user.user_profile_setname(token, "Robbie", "Caldwell") #changes both names
    assert(profile['user']['name_first'] == 'Robbie')
    assert(profile['user']['name_last'] == 'Caldwell')
    assert(profile['user']['handle_str'] == 'hjacobs') #shows that it is the same profile
        
        
def test_token_incorrect():
    login = auth.auth_register("cs1531@cse.unsw.edu.au", "123456", 
    "Hayden", "Jacobs")

    auth.auth_login("cs1531@cse.unsw.edu.au", "123456")

    token = login['token']
    u_id = login['u_id']
    user.user_profile_sethandle(token, "hjacobs")

    profile = user.user_profile(token, u_id)
    with pytest.raises(InputError):
        user.user_profile_setname("".join((token, 'wrong')), "Robbie", "Caldwell")
        
