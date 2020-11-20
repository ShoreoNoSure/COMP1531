#pylint: disable=len-as-condition
#pylint: disable=too-many-arguments
'''Functions for user/'''
import urllib
import os
import uuid
from io import BytesIO
import requests
from PIL import Image
from flask import url_for
from error import InputError
from helper import get_data, check_token, check, get_user_from_token


def user_profile(token, u_id):
    '''
    For a valid user, returns information about their
    user id, email, first name, last name, handle, and image profile URL

    Parameters:
        token - The user's token that was generated from their user id
        u_id - The profile id number to be checked

    Returns:
        An dictionary containing all the users information

    Errors:
        InputError:
            Given a u_id for a non-existent user
    '''
    check_token(token)
    data = get_data()
    # Finding the user
    for user in data['users']:
        if user['u_id'] == u_id:
            profile = {
                'u_id': u_id,
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'profile_img_url': user['profile_img_url']
            }
            return {
                'user': profile
            }
    # If u_id hasn't been found then it is obviously invalid
    raise InputError(description="Invalid u_id")

def user_profile_setname(token, name_first, name_last):
    '''
    Update the authorised user's first and last name

    Parameters:
        token - The user's token that was generated from their user id
        handle_str - The handle the user wants to change to

    Returns:
        An empty dictionary

    Errors:
        InputError:
            Either name is greater than 50 characters
            Either name is less than 1 characters
    '''
    check_token(token)
    data = get_data()
    # Checking if the name is too long or short
    if len(name_first) > 50 or len(name_last) > 50:
        raise InputError(description="Name is too long. Maximum characer length 50.")
    if len(name_first) < 1 or len(name_last) < 1:
        raise InputError(description="Name is too short. Minimum character length 1.")
    # Setting the name
    u_id = get_user_from_token(token)
    for user in data['users']:
        if user['u_id'] == u_id:
            user['name_first'] = name_first
            user['name_last'] = name_last
    return {
    }

def user_profile_setemail(token, email):
    '''
    Update the authorised user's email address

    Parameters:
        token - The user's token that was generated from their user id
        email - The email the user wants to change to

    Returns:
        An empty dictionary

    Errors:
        InputError:
            The email is an invalid email
            The email has already been taken by another user
    '''
    check_token(token)
    data = get_data()
    # Checking if the email is valid
    if not check(email):
        raise InputError(description="Invalid email")
    # Checking if email is taken
    for user in data['users']:
        if user['email'] == email:
            raise InputError(description="Email is already taken")
    # Setting the email
    u_id = get_user_from_token(token)
    for user in data['users']:
        if user['u_id'] == u_id:
            user['email'] = email
    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    Update the authorised user's handle (i.e. display name)

    Parameters:
        token - The user's token that was generated from their user id
        handle_str - The handle the user wants to change to

    Returns:
        An empty dictionary

    Errors:
        InputError:
            The handle name is greater than 20 characters
            The handle name is less than 2 characters
    '''
    check_token(token)
    data = get_data()
    # Checking if the handle is too long or short
    if len(handle_str) > 20:
        raise InputError(description="Handle is too long. Maximum characer length 20.")
    if len(handle_str) < 2:
        raise InputError(description="Handle is too short. Minimum character length 2.")
    #Check if handle is already taken by another user
    for user in data['users']:
        if user['handle_str'] == handle_str:
            raise InputError(description="Handle is already taken")
    # Setting the handle
    u_id = get_user_from_token(token)
    for user in data['users']:
        if user['u_id'] == u_id:
            user['handle_str'] = handle_str
    return {
    }

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Given a URL of an image on the internet, crops the image within bounds
    (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left

    Parameters:
        token - The user's token that was generated from their user id
        img_url - The url containing the image the user wants to upload as their profile picture
        x_start - The left side of the area the user wishes to crop the photo at the url
        x_end - The right side of the area the user wishes to crop the photo at the url
        y_start - The top of the area the user wishes to crop the photo at the url
        y_end - The bottom of the area the user wishes to crop the photo at the url

    Returns:
        An empty dictionary

    Errors:
        InputError:
            The img_url returns a non 200 response
            The image at the url is not a jpg
            The start values for the crop are greater then or equal to then end values
            One of the values given for the crop are outside the bounds of the photo
    '''
    check_token(token)
    data = get_data()
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    filename = 'images/' + uuid.uuid4().hex + '.jpg'
    response = requests.get(img_url)
    if not response.status_code == 200:
        raise InputError(description="img_url does not return a 200 status code")
    urllib.request.urlretrieve(img_url, 'static/' + filename)
    img = Image.open(BytesIO(response.content))
    if img.format != ('JPEG' or 'JPG' or 'jpg' or 'jpeg'):
        raise InputError(description="Image is not a JPG")
    width, height = img.size
    if x_start >= x_end or y_start >= y_end:
        raise InputError(description="End coordinates must be greater that start coordinates ")
    if  ((x_start or y_start or x_end or y_end) < 0 or
         (x_start or x_end) > width or (y_start or y_end) > height):
        raise InputError(description="Crop is not within the bounds of the image")
    area = (x_start, y_start, x_end, y_end)
    img = img.crop(area)
    img.save('static/' + filename)
    u_id = get_user_from_token(token)
    img_url = url_for('static', filename=filename, _external=True)
    for user in data['users']:
        if user['u_id'] == u_id:
            user['profile_img_url'] = img_url
    return {
    }
