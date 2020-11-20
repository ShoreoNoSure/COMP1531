import urllib.request
import json

BASE_URL = "http://127.0.0.1:8963"
def test_basic():
    # Check if the names are empty
    response = urllib.request.urlopen(f"{BASE_URL}/names")
    payload = json.load(response)
    assert payload['names'] == []

def test_add():
    data = json.dumps({'name': 'Hayden'}).encode('utf-8')
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/name/add",
        data=data,
        headers={'Content-Type': 'application/json'}
    ))
    payload = json.load(response)

    response = urllib.request.urlopen(f"{BASE_URL}/names")
    payload = json.load(response)
    assert payload['names'] == ['Hayden']

def test_remove():
    data = json.dumps({'name': 'Hayden'}).encode('utf-8')
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/name/remove",
        data=data,
        headers={'Content-Type': 'application/json'},
        method='DELETE'
    ))
    payload = json.load(response)

    response = urllib.request.urlopen(f"{BASE_URL}/names")
    payload = json.load(response)
    assert payload['names'] == []

def test_complex():
    data = json.dumps({'name': 'Sinha'}).encode('utf-8')
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/name/add",
        data=data,
        headers={'Content-Type': 'application/json'}
    ))
    payload = json.load(response)

    data = json.dumps({'name': 'Roy'}).encode('utf-8')
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/name/add",
        data=data,
        headers={'Content-Type': 'application/json'}
    ))
    payload = json.load(response)

    data = json.dumps({'name': 'Hayden'}).encode('utf-8')
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/name/add",
        data=data,
        headers={'Content-Type': 'application/json'}
    ))
    payload = json.load(response)

    data = json.dumps({'name': 'Hayden'}).encode('utf-8')
    response = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/name/remove",
        data=data,
        headers={'Content-Type': 'application/json'},
        method='DELETE'
    ))
    payload = json.load(response)

    response = urllib.request.urlopen(f"{BASE_URL}/names")
    payload = json.load(response)
    assert payload['names'] == ['Sinha', 'Roy']
    