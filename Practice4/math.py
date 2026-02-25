#1Write a Python program to convert degree to radian.
import math
degree = float(input("Input degree: "))
#radian = degree * π / 180
radian = degree * math.pi / 180
print(f"Output radian: {radian}")



#2Write a Python program to calculate the area of a trapezoid.
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
# Formula: Area = ½ × (base1 + base2) × height
area = 0.5 * (base1 + base2) * height
print(f"Expected Output: {area}")



#3Write a Python program to calculate the area of regular polygon.
import math
sides = int(input("Input number of sides: "))
side_length = float(input("Input the length of a side: "))
# Formula: Area = (n × s²) / (4 × tan(π/n))
area = (sides * side_length ** 2) / (4 * math.tan(math.pi / sides))
print(f"The area of the polygon is: {round(area)}")



#4Write a Python program to calculate the area of a parallelogram.
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
# Formula: Area = base × height
area = base * height
print(f"Expected Output: {area}")