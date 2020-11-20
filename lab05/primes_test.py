import primes

def test_prime():
    assert primes.factors(17) == [17]

def test_two_factors():
    assert primes.factors(39) == [3, 13]

def test_more_factors():
    assert primes.factors(68) == [2, 2, 17]

def test_zero():
    assert primes.factors(0) == []
