def divisors(n):
    '''
    Given some number n, return a set of all the numbers that divide it. For example:
    >>> divisors(12)
    {1, 2, 3, 4, 6, 12}

    Params:
      n (int): The operand

    Returns:
      (set of int): All the divisors of n

    Raises:
      ValueError: If n is not a positive integer
    '''
    if n < 0:
      raise ValueError
    elif n == 0:
      return {0}
    factor = 2
    factors = {1}
    while factor <= n:
      if n % factor == 0:
        factors.add(factor)
      factor += 1
    return factors

    
