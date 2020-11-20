import sys

def cal_bmi(weight, height):
    return weight/(height*height)
    
    
if __name__ == "__main__":
    print("What is your weight in kg?")
    weight = int(input())
    print("What is your height in m?")
    height = float(input())
    bmi = cal_bmi(weight, height)
    print("Your bmi is %.1f" %bmi)
    
    
