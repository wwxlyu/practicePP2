# Example 1: Simple lambda that adds two numbers
add = lambda a, b: a + b
print(add(3, 5))

# Example 2: Lambda that squares a number
square = lambda x: x ** 2
print(square(6))

# Example 3: Lambda with conditional expression
is_even = lambda n: "Even" if n % 2 == 0 else "Odd"
print(is_even(7))

# Example 4: Lambda returning a string in uppercase
uppercase = lambda s: s.upper()
print(uppercase("hello"))

# Example 5: Lambda with multiple operations
calculate = lambda x, y: x**2 + y**2
print(calculate(2, 3))
