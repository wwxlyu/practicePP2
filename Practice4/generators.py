#1Create a generator that generates the squares of numbers up to some number N.
def squares_generator(n):
    for i in range(1, n + 1):
        yield i * i
#Test
n = int(input("Enter n: "))
for square in squares_generator(n):
    print(square)



#2Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.
def even_generator(n):
    for i in range(0, n + 1, 2):
        yield i
# Test
n = int(input("Enter n: "))
result = []
for num in even_generator(n):
    result.append(str(num))
print(','.join(result))



#3 Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.
def divisible_generator(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
#Test
n = int(input("Enter n: "))
for num in divisible_generator(n):
    print(num, end=' ')



#4Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i
#Test
a = int(input("Enter a: "))
b = int(input("Enter b: "))
for square in squares(a, b):
    print(square)



#5Implement a generator that returns all numbers from (n) down to 0.
def countdown(n):
    for i in range(n, -1, -1):
        yield i
# Test
n = int(input("Enter n: "))
for num in countdown(n):
    print(num)