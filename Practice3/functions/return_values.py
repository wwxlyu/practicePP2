# Example 1: Simple return
def multiply(a, b):
    return a * b
print(multiply(3, 4))

# Example 2: Returning a string
def greet(name):
    return f"Hello, {name}!"
print(greet("Alice"))

# Example 3: Returning multiple values
def stats(numbers):
    return sum(numbers), len(numbers), sum(numbers)/len(numbers)
print(stats([2, 4, 6, 8]))

# Example 4: Returning a list
def squares(nums):
    return [n**2 for n in nums]
print(squares([1, 2, 3, 4]))

# Example 5: Returning a boolean
def is_positive(n):
    return n > 0
print(is_positive(-5))
