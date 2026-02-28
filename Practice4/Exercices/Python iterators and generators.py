#1
def squares(n):
    for i in range(n + 1):
        yield i * i

for x in squares(5):
    print(x)

#2
def even_numbers(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield i

n = int(input())

print(",".join(str(x) for x in even_numbers(n)))

#3
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i

for x in divisible_by_3_and_4(100):
    print(x)

#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

a = int(input())
b = int(input())

for x in squares(a, b):
    print(x)

#5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

for x in countdown(5):
    print(x)