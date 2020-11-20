president = {
    'name' : 'Ian Jacobs',
    'age' : 54,
    'staff' : [ 'Sally', 'Bob', 'Rob', 'Hayden' ]
}

## TODO: Write code below this line

if __name__ == '__main__':
    del president['staff'][3]

    marks = {
        "20T1": 77,
        "20T2": 88,
        "20T3": 99,
    } 
    president['staff'].sort()
    president['marks'] = marks
    print(president)

## TODO: Write code above this line
