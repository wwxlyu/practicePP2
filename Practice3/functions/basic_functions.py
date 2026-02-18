# Example 1: Simple function to greet
def greet():
    print("Hello, world!")
greet()

# Example 2: Function to add two numbers
def add_numbers(a, b):
    return a + b
print(add_numbers(3, 5))

# Example 3: Function to check even/odd
def is_even(n):
    if n % 2 == 0:
        print(f"{n} is even")
    else:
        print(f"{n} is odd")
is_even(7)

# Example 4: Function without parameters printing a message
def favorite_language():
    print("My favorite language is Python")
favorite_language()

# Example 5: Function using a local variable
def square_number(num):
    result = num ** 2
    return result
print(square_number(6))
