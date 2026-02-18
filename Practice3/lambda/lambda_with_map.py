# Example 1: Square numbers in a list using map
nums = [1, 2, 3, 4]
squared = list(map(lambda x: x**2, nums))
print(squared)

# Example 2: Convert list of strings to uppercase
words = ["apple", "banana", "cherry"]
upper_words = list(map(lambda w: w.upper(), words))
print(upper_words)

# Example 3: Add 10 to each element
nums = [5, 10, 15]
plus_ten = list(map(lambda n: n + 10, nums))
print(plus_ten)

# Example 4: Multiply two lists element-wise
a = [1,2,3]; b = [4,5,6]
multiplied = list(map(lambda x, y: x*y, a, b))
print(multiplied)

# Example 5: Convert list of numbers to string
numbers = [1, 2, 3]
str_numbers = list(map(lambda n: str(n), numbers))
print(str_numbers)
