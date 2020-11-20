'''
pick_word - Picks the word
print_hangman - Prints the hangman
start_game - Starts the game
check_word - Checks the word
'''
import random
import linecache
from error import AccessError, InputError
from helper import get_data, check_token
# built in dict source: /usr/share/dict/british-english
# pick_word: Refer to https://ubuntuforums.org/showthread.php?t=673569
#pylint: disable = anomalous-backslash-in-string
#pylint: disable = too-many-branches
def pick_word():
    '''
    Search from /usr/share/dict/british-english, return a random word (str)

    Parameters:

    Returns:
        The word to guess for the game

    Errors:
    '''
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    source = '/usr/share/dict/british-english'
    num_words = len((open(source).readlines()))
    word = linecache.getline(source, random.randint(0, num_words - 1)).strip()
    if len(word) > 1:
        # Avoid words with ' etc. marks.
        for letter in word:
            if letter not in alphabet:
                return pick_word()
        return word
    return pick_word()

def print_hangman(tries):
    '''
    Input the number of tries left, return the corresponding image of hangman as string

    Parameters:
        tries - Number of tries left to guess

    Returns:
        The hangman image

    Errors:
    '''
    if tries == 10:
        return ''
    hangman_image = ['__', '|\n|\n|\n|\n|_\n', '_ _ _\n|\n|\n|\n|\n|_\n', \
    '_ _ _ \n |' + ' ' + ' | \n  | \n  | \n  | \n|_ \n', \
    '_ _ _ \n |' + ' ' + ' | \n  |  O \n  | \n  | \n|_ \n', \
    '_ _ _ \n |' + ' ' + ' | \n  |  O \n  |  | \n  | \n|_ \n', \
    '_ _ _ \n |' + ' ' + ' | \n  |  O \n  | /| \n  | \n|_ \n', \
    '_ _ _ \n |' + ' ' + ' | \n  |  O \n  | /|\ \n  | \n|_ \n', \
    '_ _ _ \n |' + ' ' + ' | \n  |  O \n  | /|\ \n  | / \n|_ \n', \
    '_ _ _ \n |' + ' ' + ' | \n  |  O \n  | /|\ \n  | / \ \n|_ \n',]
    return hangman_image[9 - tries]

def start_game(token, channel_id):
    '''
    Start the game, initialise hangman package for this channel, add package to the database

    Parameters:
        token - The user's token that was generated from their user id
        channel_id - The id of the channel to play the game in

    Returns:
        A message ready to be posted by hangman bot

    Errors:
    '''
    # check if user is valid
    check_token(token)
    # check if the game is already active
    data = get_data()
    for package in data['hangman']:
        if package['channel_id'] == channel_id:
            if package['is_active'] is True:
                raise AccessError(description='There is already an active game in this channel.')
            # delete/reset package
            data['hangman'].remove(package)

    picked = pick_word()
    hangman_package = {
        'channel_id': channel_id,
        'is_active': True,
        'guessed': False,
        'word': picked,
        'letters_guessed': [],
        'tries': 10
    }
    data['hangman'].insert(0, hangman_package)
    return 'The word contains ' + str(len(picked)) + ' letters.\n' + len(picked) * '_'

def check_word(token, guess, channel_id):
    '''
    Check if the guessed letter is inside the picked word, \
    or if the guessed word matches the picked word

    Parameters:
        token - The user's token that was generated from their user id
        guess - The letter or word which the user guesses
        channel_id - The id of the channel in which the game is played in

    Returns:
        A message ready to be posted by hangman bot
    '''
    check_token(token)
    data = get_data()
    hangman_package = {}
    for package in data['hangman']:
        if package['channel_id'] == channel_id:
            if package['is_active'] is False:
                raise AccessError(description='These is no active game in this channel.')
            hangman_package = package

    # No such hangman game active in this channel
    if hangman_package == {}:
        raise InputError(description='There is no active hangman game in this channel.')
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    checked_result = ''
    #1 - user inputs a letter
    if len(guess) == 1:
        if guess not in alphabet:
            checked_result += 'You have not entered a letter.'
        elif guess not in hangman_package['word']:
            hangman_package['letters_guessed'].append(guess)
            hangman_package['tries'] -= 1
        elif guess in hangman_package['word']:
            hangman_package['letters_guessed'].append(guess)

    #2 - user inputs the full word
    elif len(guess) == len(hangman_package['word']):
        if guess == hangman_package['word']:
            checked_result += 'Well done, you have guessed the word! :)'
            hangman_package['guessed'] = True
        else:
            hangman_package['tries'] -= 1
    #3 - user inputs a word that is not of the length of the picked word
    else:
        checked_result += 'The length of the word you entered is not the length we want.'

    checked_result += '\n'
    status = ''
    if hangman_package['guessed'] is False:
        for letter in hangman_package['word']:
            if letter in hangman_package['letters_guessed']:
                status += letter
            else:
                status += '_'
        checked_result += status
        checked_result += '\n'

    if status == hangman_package['word']:
        checked_result += 'Well done, you have guessed the word! :)\n'
        hangman_package['guessed'] = True
        hangman_package['is_active'] = False
        return checked_result

    if hangman_package['tries'] == 0:
        checked_result += 'You have run out of guesses and you haven\'t guessed the word. :(\n'
        checked_result += 'The word is ' + hangman_package['word'] + '.\n'
        hangman_package['is_active'] = False

    return checked_result + print_hangman(hangman_package['tries'])
