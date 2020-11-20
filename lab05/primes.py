import math

#Find all prime factors of num
def factors(num):
    store = []
    if num == 0:
        return []
  #Check if 2 divide num
  #Add the number of 2 to the factor list
    while num % 2 == 0:
        store.append(2)
        num = num / 2

  # num must be odd at this point
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        while num % i == 0:
            store.append(i)
            num = num / i

#If num is greater than 2 now, it is a prime number
    if num > 2:
        store.append(int(num))

    return store

if __name__ == "__main__":
    #make input str an int
    print(' '.join(str(x) for x in factors(int(input))))
