# Lab 06

## Due: Week **8**, Sunday, 4:59 pm

## Value: 2 marks

## Setup

An individual repository for this lab has been created for you here (replace z5555555 with your own zID):

https://gitlab.cse.unsw.edu.au/z5555555/20T1-cs1531-lab07

## Exercise 1

Consider the rainfall problem from your week 2 tutorial

> Given a list of integers, compute the average of only the positive elements.

Implement this as the function `rainfall(...)` in `rainfall.py`. Do this without adding any additional import statements or using any form of `for` or `while` structure. This includes conventional loops as well as list comprehensions. Basically, the keywords `for` or `while` cannot appear anywhere in the file. Similarly, you should not use any form of recursion.

## Exercise 2

Included in `point.py` is an example from the lectures. The class `Point` *stores* a point in polar form (`theta` and `r`), but allows for *use* as a cartesian (`x` and `y`) point as well. It does this using Python *properties*. Modify the example so it does the reverse of this. It should store the point in cartesian form, but allow for use in polar form. Any code that used the class previously, like the included `distance(...)` and `test_point()` functions should not require any change. Ensure that the test `test_point()` still passes after your modifications.

## Exercise 3

Complete the class `Stack` in `stack.py`, ensuring the only publicly exposed attributes are the methods `push(...)` and `pop()`.

## Exercise 4 (challenge)

In addition to being able to apply a function to all elements of a single list, the `map(...)` function can be used to apply a function to each pair of elements from two lists. For example,

```python
>>> list(map(lambda a, b: a + b, [1,2,3], [4,5,6]))
[5,7,9]
```

Using this fact, implement the `transpose(...)` function in `transpose.py` according to its documentation. Once again, like exercise 1, you should not add any more import statements, the keywords `for` and `while` should not appear anywhere in the file, and recursion should not be used.

## Submission

Make sure that all your work has been pushed to GitLab then submit it with:

```bash
$ 1531 submit lab07
```
