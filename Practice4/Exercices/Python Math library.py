import math
#1
degree = float(input("Input degree: "))

radian = degree * math.pi / 180

print("Radian:", radian)

#2
a = float(input("Base 1: "))
b = float(input("Base 2: "))
h = float(input("Height: "))

area = (a + b) / 2 * h

print("Area:", area)

#3
n = int(input())
a = float(input())

area = (n * a * a) / (4 * math.tan(math.pi / n))
print(area)

#4
base = float(input())
height = float(input())

area = base * height
print(area)