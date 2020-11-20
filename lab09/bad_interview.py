def bad_interview():
    '''
    A generator that yields all numbers from 1 onward, but with some exceptions:
    * For numbers divisible by 3 it instead yields "Fizz"
    * For numbers divisible by 5 it instead yields "Buzz"
    * For numbers divisible by both 3 and 5 it instead yields "FizzBuzz"
    '''
    base = 1
    while True:
        if base % 3 == 0 and base % 5 == 0:
            yield "FizzBuzz"     
        elif base % 3 == 0:
            yield 'Fizz'
        elif base % 5 == 0:
            yield 'Buzz'
        else:
            yield base
        base += 1 
        
