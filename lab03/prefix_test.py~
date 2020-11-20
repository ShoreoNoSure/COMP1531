from prefix import prefix_search
import pytest

def test_documentation():
    assert prefix_search({'ac': 1, 'ba': 2, 'ab': 3}, 'a') == { 'ac': 1, 'ab': 3}

def test_exact_match():
    assert prefix_search({'category': 'math', 'cat': 'animal'}, 'cat') == {'category': 'math', 'cat': 'animal'}

def test_no_match():
    with pytest.raises(KeyError):
        prefix_search({'student': 'Mich', 'Phone': '0044123442'}, 'Home')

def test_number_prefix():
    assert prefix_search({'1': 'cents', '2': 'dolars', '3': 'notes'}, '2') == {'2': 'dolars'} 
