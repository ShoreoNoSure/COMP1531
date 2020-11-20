from json import dumps
from flask import Flask, request

APP = Flask(__name__)

DATASTORE = {}

def get_store():
    '''Create a new dictionary for storing data'''
    global DATASTORE
    return DATASTORE

def reset_store():
    '''Reset DATASTORE to empty'''
    global DATASTORE
    DATASTORE = {
        'names': []
    }

@APP.route("/name/add", methods=['POST'])
def name_add():
    '''add a new name'''
    data = request.get_json()
    store = get_store()
    store['names'].append(data['name'])
    return dumps({})

@APP.route("/names", methods=['GET'])
def names():
    '''return a name list'''
    store = get_store()
    return dumps({
        'names': store['names']
    })

@APP.route("/name/remove", methods=['DELETE'])
def name_remove():
    '''delete a name from list'''
    data = request.get_json()
    store = get_store()
    store['names'].remove(data['name'])
    return dumps({})

if __name__ == "__main__":
    reset_store()
    APP.run(port=8963)
