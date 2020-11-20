def balanced(n):
    '''
    Given a positive number n, compute the set of all strings of length n, in any order, that only
    contain balanced brackets. For example:
    >>> balanced(6)
    {'((()))', '(()())', '(())()', '()(())', '()()()'}

    Note that, by definition, the only string of length 0 containing balanced brackets is the empty
    string.

    Params:
      n (int): The length of string we want

    Returns:
      (set of str): Each string in this set contains balanced brackets. In the event n is odd, this
      set is empty.

    Raises:
      ValueError: If n is negative
    '''
    if n < 0:
      raise ValueError
    elif n == 0 or n % 2 == 1: 
      return {}
    
    table = [['']]
    for j in range(1, n + 1):
        result = []
        for i in range(j):
            for x in table[i]:
                for y in table[j - i - 1]:
                    result.append('(' + x + ')' + y)
        table.append(result)
    res = {}
    for item in table[n]:
      res.add(item)
    return res





      
