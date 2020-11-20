# Lab 06

## Due: Week **7**, Wednesday, 4:59 pm

## Value: 2 marks

## Setup

An individual repository for this lab has been created for you here (replace z5555555 with your own zID):

https://gitlab.cse.unsw.edu.au/z5555555/20T1-cs1531-lab06

## Exercise 1

A pickled file with data in it is stored in `shapecolour.p`. Write a program `unpickle.py` that un-pickles this file, and analyses the data to print what the most common shape-colour pair is.

The output of `unpickle.py` should be (for example, if the most common dictionary pair is red circle):

```txt
Colour: red
Shape: circle
```

Ensure your code is pylint compliant.

## Exercise 2

With the unpickled files from exercise 1, wrap the shape colour data in a bigger data structure:

```json
{
    "mostCommon" : {
        "colour" : "[most-common-colour]",
        "shape" : "[most-common-shape]"
    },
    "rawData" : [insert-raw-data-from-shapecolour.p]
}
```

[Items in brackets] should be replaced with actual values or data structures.

Write a file `process.py` that creates this new data structure, then outputs it as JSON to a file `processed.json`

Ensure your code is pylint compliant.

## Exercise 3

Convert the JSON file `data_1.json` to YAML in `data_1.yml`
Convert the YAML file `data_2.yml` to JSON in `data_2.json`

Of course, you can do this with [simple online tools](https://www.json2yaml.com/). However, we encourage you to try and do this manually because during the exam if we test you on these items you need to be prepared!

## Exercise 4

Copy the weather data from week 3 lectures.

```bash
cp ~cs1531/public_html/20T1/weatherAUS.csv ./
```

Write a program `weather.py` that takes in a command line argument that is the date in format DD-MM-YYYY and the name of the town, for example

```bash
python3 weather.py "08-08-2010" "Albury"
```

If an invalid (or empty) date or town is entered, the program should simply print
```txt
Invalid input
```

If valid inputs are entered, the program should print the difference between the MinTemp and MaxTemp on that day, and the average minimum temperature and average maximum temperature over the entire date range for that town.

For example, if the MinTemp and MaxTemp of Albury on 08-08-2010 is -1.3 and 12.6 respectively, and the average minimum and average maximum temperature of Albury over the entire data set is 9.5 and 22.6, the program would output:

```bash
$ python3 weather.py "08-08-2010" "Albury"
MinTemp is 10.8 degrees below average minimum
MaxTemp is 10.0 degrees below average maximum
```

Round all final results to 1 decimal place. Any values in the table that are "NA" or any other invalid number do not need to be counted.

Ensure your code is pylint compliant.

## Exercise 5

Implement the `reduce` function in `reduce.py`.

The `reduce` function takes a function and a list and applies the function over the list:

`reduce(f, xs)` takes the first two values from the list `xs`, and uses it as the parameters to call the function `f`. It feeds the return value from the function `f` and the next value from the list back in to the function `f` and repeats until the list `xs` is empty. If the list only has one element then it returns the first element. If the list is empty then it returns None.

```bash
reduce(f, [1,2,3,4,5])                  -> f(f(f(1,2),3),4,5)
reduce(f, [])                           -> None
reduce(f, [1])                          -> 1

reduce(lambda x, y: x + y, [1,2,3,4,5]) -> 15
reduce(lambda x, y: x + y, 'abcdefg')   -> 'abcdefg'
reduce(lambda x, y: x * y, [1,2,3,4,5]) -> 120
```

Write pytests for your reduce function in `reduce_test.py` and ensure they have 100% coverage. Ensure your code is pylint compliant.

## Exercise 6 (Bonus / Challenge)

You are not expected to complete this exercise.

Setup a flask server `imgsneak.py` that serves a 1px x 1px transparent png at a path /email/img.png?code=ABCDEFG

Where ABCDEFG is a unique code that can be anything.

When this route is accessed (via GET method), the unique code ABCDEFG should be printed to terminal.

Demonstrate to your tutor how you can send yourself an email (via any email account on the CSE machine) with an image in the email and how when they open the email your running flask server prints out the code.

Note: (you'll have to send a raw email with the code:
```html
<img src="http://127.0.0.1/email/img.png?code=yourname" />
```

## Exercise 7 (Bonus / Challenge)

Write a program which:
 * Creates a class named Circle that has one attribute r (for radius) and two instance methods: circumference (which returns the circumference of the circle) and area (which returns the area of the circle).
 * Asks the user for a radius (integer), then, using Circle, tells the user the circumference and area of a circle with that radius, both to 1 decimal place.

```bash
Please enter a radius: 5
Circumference: 31.4
Area: 78.5
```

## Submission

Make sure that all your work has been pushed to GitLab then submit it with:

```bash
$ 1531 submit lab06
```
