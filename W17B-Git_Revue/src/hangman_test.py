#pylint: disable = missing-docstring, line-too-long, anomalous-backslash-in-string
'''This is a test file for hangman.py'''
import pytest
from error import AccessError, InputError
from hangman import check_word, start_game
from auth import auth_register
from channels import channels_create
from helper import get_data, reset_data

def test_start_game_success():
    reset_data()
    data = get_data()
    user = auth_register('z5261703@unsw.edu.au', 'ilovecse', 'Jiaqi', 'Zhu')
    test_channel = channels_create(user['token'], 'test channel 1', True)
    start_game(user['token'], test_channel['channel_id'])
    assert data['hangman'][0]['is_active'] is True

def test_check_word_simbol():
    reset_data()
    data = get_data()
    user = auth_register('z5261703@unsw.edu.au', 'ilovecse', 'Jiaqi', 'Zhu')
    test_channel = channels_create(user['token'], 'test channel 1', True)
    hangman_package = {
        'channel_id': test_channel['channel_id'],
        'is_active': True,
        'guessed': False,
        'word': 'hello',
        'letters_guessed': [],
        'tries': 10
    }
    data['hangman'].append(hangman_package)
    assert check_word(user['token'], '?', 1) == 'You have not entered a letter.\n_____\n'

def test_game_already_active():
    reset_data()
    user = auth_register('z5261703@unsw.edu.au', 'ilovecse', 'Jiaqi', 'Zhu')
    test_channel = channels_create(user['token'], 'test channel 1', True)
    start_game(user['token'], test_channel['channel_id'])
    with pytest.raises(AccessError):
        start_game(user['token'], test_channel['channel_id'])

def test_no_active_game():
    reset_data()
    user = auth_register('z5261703@unsw.edu.au', 'ilovecse', 'Jiaqi', 'Zhu')
    test_channel = channels_create(user['token'], 'test channel 1', True)
    with pytest.raises(InputError):
        check_word(user['token'], 'h', test_channel['channel_id'])

def test_guess_word():
    reset_data()
    data = get_data()
    user = auth_register('z5261703@unsw.edu.au', 'ilovecse', 'Jiaqi', 'Zhu')
    test_channel = channels_create(user['token'], 'test channel 1', True)
    hangman_package = {
        'channel_id': test_channel['channel_id'],
        'is_active': True,
        'guessed': False,
        'word': 'hello',
        'letters_guessed': [],
        'tries': 10
    }
    data['hangman'].append(hangman_package)
    check_word(user['token'], 'a', 1)
    check_word(user['token'], 'b', 1)
    check_word(user['token'], 'c', 1)
    check_word(user['token'], 'e', 1)
    check_word(user['token'], 'd', 1)
    check_word(user['token'], 'o', 1)
    check_word(user['token'], 't', 1)
    check_word(user['token'], 'n', 1)
    check_word(user['token'], 'k', 1)
    check_word(user['token'], 'm', 1)
    check_word(user['token'], 'p', 1)
    assert check_word(user['token'], 'q', 1) == '\n_e__o\nYou have run out of guesses and you haven\'t guessed the word. :(\nThe word is hello.\n_ _ _ \n |' + ' ' + ' | \n  |  O \n  | /|\ \n  | / \ \n|_ \n'
