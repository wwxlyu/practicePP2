# Example 1: Filter even numbers
nums = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)

# Example 2: Filter strings longer than 4 characters
words = ["apple", "cat", "banana", "dog"]
long_words = list(filter(lambda w: len(w) > 4, words))
print(long_words)

# Example 3: Filter numbers greater than 10
nums = [5, 12, 8, 20]
gt_ten = list(filter(lambda n: n > 10, nums))
print(gt_ten)

# Example 4: Filter negative numbers
numbers = [-5, 3, -1, 0, 2]
negatives = list(filter(lambda x: x < 0, numbers))
print(negatives)

# Example 5: Filter words starting with 'a'
words = ["apple", "banana", "avocado", "cherry"]
a_words = list(filter(lambda w: w.startswith('a'), words))
print(a_words)
