import auth
import other
import user
import pytest

# Test with one user
def test_users_all_simple():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Giving all the users' profile details
    assert other.users_all(user_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'm@gmail',
                'name_first': 'name',
                'name_last': 'lastname',
                'handle_str': 'namelastname',
            }
        ],

    }

# Test with multiple users
def test_users_all_complex():
    user1_info = auth.auth_register('a@gmail', 'sadsad', 'aName', 'aLastname')
    user2_info = auth.auth_register('b@gmail', 'sadsad', 'bName', 'bLastname')
    user3_info = auth.auth_register('c@gmail', 'sadsad', 'cName', 'cLastname')
    # Giving all the users' profile details
    assert other.users_all(user1_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'a@gmail',
                'name_first': 'aName',
                'name_last': 'aLastname',
                'handle_str': 'anamealastname',
            },
            {
                'u_id': 2,
                'email': 'b@gmail',
                'name_first': 'bName',
                'name_last': 'bLastname',
                'handle_str': 'bnameblastname',
            },
            {
                'u_id': 3,
                'email': 'c@gmail',
                'name_first': 'cName',
                'name_last': 'cLastname',
                'handle_str': 'cnameclastname',
            }
        ],

    }

# Test with a changed name
def test_users_all_newname():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Changing name
    user.user_profile_setname(user_info['token'], "newname", "newlastname")
    # Giving all the users' profile details
    assert other.users_all(user_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'm@gmail',
                'name_first': 'newname',
                'name_last': 'newlastname',
                'handle_str': 'namelastname',
            }
        ],

    }

# Test with a changed email WIP
def test_users_all_newemail():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Changing email
    user.user_profile_setemail(user_info['token'], "newm@gmail")
    # Giving all the users' profile details
    assert other.users_all(user_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'newm@gmail',
                'name_first': 'name',
                'name_last': 'lastname',
                'handle_str': 'namelastname',
            }
        ],

    }

# Test with a changed handle
def test_users_all_newhandle():
    user_info = auth.auth_register('m@gmail', 'sadsad', 'name', 'lastname')
    # Changing handle
    user.user_profile_sethandle(user_info['token'], "newhandle")
    # Giving all the users' profile details
    assert other.users_all(user_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'm@gmail',
                'name_first': 'name',
                'name_last': 'lastname',
                'handle_str': 'newhandle',
            }
        ],

    }

# Test when a user has logged out
def test_users_all_complex():
    user1_info = auth.auth_register('a@gmail', 'sadsad', 'aName', 'aLastname')
    user2_info = auth.auth_register('b@gmail', 'sadsad', 'bName', 'bLastname')
    # User2 logs out
    auth.auth_logout(user2_info['token'])
    # Giving all the users' profile details
    assert other.users_all(user1_info['token']) == {
        'users': [
            {
                'u_id': 1,
                'email': 'a@gmail',
                'name_first': 'aName',
                'name_last': 'aLastname',
                'handle_str': 'anamealastname',
            },
            {
                'u_id': 2,
                'email': 'b@gmail',
                'name_first': 'bName',
                'name_last': 'bLastname',
                'handle_str': 'bnameblastname',
            },
        ],

    }