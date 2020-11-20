'''
TODO Complete this file by following the instructions in the lab exercise.
'''

strings = ['This', 'list', 'is', 'now', 'all', 'together']
result = ''
for idx in range(0,len(strings)):
    if idx == len(strings) - 1:
        result += strings[idx]
    else:
        result += strings[idx] + " "
    idx += 1
print (result)
print(' '.join(strings))
