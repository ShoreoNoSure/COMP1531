import sys

def roman(input):
	numerals = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}

	res = 0
	for i in range(len(input)):
		value = numerals[input[i]]
		if i + 1 < len(input) and numerals[input[i+1]] > value:
			res -= value
		else: 
			res += value
	return res

def test_empty():
    assert roman("") == 0
    	
def test_single():
    assert roman('M') == 1000
    assert roman('D') == 500
    assert roman('C') == 100

def test_add_only():
    assert roman("CC") == 200
    assert roman("MDXI") == 1511
    assert roman("MMCCCXXIII") == 2323
    
def test_minus_only():
    assert roman("IM") == 999
    assert roman("XC") == 90
    assert roman("VD") == 495

def test_mixed():
    assert roman("CDXXIX") == 429
    assert roman("MMDMXCVI") == 2596
    assert roman("CCXCVIII") == 298
