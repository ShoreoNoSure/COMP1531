 For all files:
 - When testing functions, it is assumed that all other functions work.
 
 In user.py:
 - For the user_profile_setname function: I am assuming that if the cases where the input for either the first or last name is too short or long is detected, then any combination of these for both names would also be detected and therefore does not need any further testing.
 
 In channels.py:
 - For the channels_create, channels_listall and channels_list functions I am assuming that a valid token will always be given.
 - For channels_list I'm assuming you cannot see Public or Private channels that you are not in
 - For channels_listall I'm assuming you cannot see Private channels that you are not in
 - For channels_create I'm assuming a channel's name will always have an input
 - For channels_create I'm assuming two channels can have the same name
 
 In channel.py:
 - For channel_invite I assume that the same person cannot be invited more than once since that person will automatically join the channel after the first invitation.
 - For channel_join I assume that the channel creator cannot join the channel they created as they are already in that channel.
 - For channel_leave I assume that the channel creator can leave the channel when there is no other assigned owners.
 - For channel_join I assume that if the owner of slackr joins the channel, he will not be added to owner_members list.
 
 In other.py:
 - For users_all it shows users even if they are logged out
 - For search I'm assuming that the search function can be called even if there have been no messages made in any channel
 - For search I'm assuming the query string will always have an input
 - For search I'm assuming the query string is not case sensitive
 - For search I'm assuming if the query string exists within a word of a message, it will be returned (eg if the query string is 'o' and the message is 'hello' the message will be retured)
 
 In message.py:
 - For message functions I assume that when another user is created there will be a new u_id
 - For message functions I assume different messages should have different ids
 - For message functions I assume that message ids are always in ascending order of their sending no matter what channel they were sent in
 - I assume that if a user is able to send a message, he must be inside a valid channel
 
 In auth.py:
 - For auth functions I assume generating u_id always starts from 1
 - I assume that a new u_id is always one plus the maximum u_id of the current slackr

 In standup.py:
 - I assume that standup is inactive when the packaged message is sent. (Since the timer runs out after the required length of time)
 - I assume that standup continues even if user is logged out.
 - I assume that system time for running the timer is not included in the actual timer at the frontend. (Otherwise we will need to add system execution time to the timer)

 In server.py:
 - I assume that any empty input should raise InputError.
 - I assume that a user cannot send empty message or guess a word in hangman game with an empty string (InputError will be raised).

 In hangman.py:
 - Assume that each channel can only have one hangman game active. Trying to use '/hangman' to start a new game will raise access error. Only when the previous game is finished, a user can then start a new game with a new random word. 
 - Assume that the picked word from the source file does not have any non-alphabetical simbols. In other word, any word with non-alphabetical simbols such as " ' " will be skipped by the program. This is designed to reduce the difficulty of the game.
 - Assume that the program can detect if a user enters a non-alphabetical simbol or some string that is of the wrong length etc., but it will not be considered as failing to guess the word, and hence that will not cause decrement in the number of tries left.
 - Assume that the input 'guess' will always be valid (has a value) as server.py will raise input error if 'guess' is empty ('').

 For hangman game regarding other functions:
 - I assume that hangman bot is a permnant user inside slackr and has all parameters like other users.
 - I assume that hangman bot is always logged in inside slackr and message_send function will not limit the bot to send out messages in any channels.
 - I assume that hangman bot messages are treated equally as messages sent by normal users.
 - I assume that hangman bot will not take valid inputs as described in the assumptions above.
 - I assume that there is no restriction on time limit of the game (it will only be inactivated once a word is guessed or once the tries are run out) or the number of people who can guess the word. All users who are logged in and who are inside the channel can participate in the hangman game. The punishment for failing to guess a letter/word will be the same for every user.
