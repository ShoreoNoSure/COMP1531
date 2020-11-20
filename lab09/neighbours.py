
def neighbours(iterable):
    '''
    A generator, that, given an iterable, yields the "neighbourhood" of each
    element. The neighbourhood is a tuple containing the element itself as well
    as the one that comes before and the one that comes after. For example,
    >>> list(neighbours([1,2,3,4]))
    [(1,2), (1,2,3), (2,3,4), (3,4)]

    Note that the first and last elements are pairs, while the rest are triples.

    Params:
      iterable (iterable): The iterable being processed. In the event it's empty,
      this generator should not yield anything. In the event it only contains
      one element, only that element should be yielded in a one-tuple.

    Yields:
      (tuple) : The neighbourhood of the current element.
    '''
    # Hint: Don't forget that iterables can produce values infinitely. You can't
    # rely on being able to retrieve all the elements at once.
    if iterable == []:
      return
    counter = 0
    for i in iterable:
      if counter == 0:
        prev = i
        mid = i
        after = i
        counter += 1
      elif counter == 1:
        mid = i
        yield prev, mid
        counter += 1
      elif counter == 2:
        after = i
        yield prev, mid, after
        counter += 1
      else:
        prev = mid
        mid = after
        after = i
        yield prev, mid, after
        counter += 1
    if counter == 1:
      yield prev, 
    elif counter == 2:
      yield prev, mid
    elif mid and after and counter > 2:
      yield mid, after
