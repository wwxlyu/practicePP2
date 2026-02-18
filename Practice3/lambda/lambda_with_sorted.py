# Example 1: Sort a list of numbers
nums = [5, 2, 9, 1]
sorted_nums = sorted(nums)
print(sorted_nums)

# Example 2: Sort strings by length
words = ["apple", "kiwi", "banana"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

# Example 3: Sort tuples by second element
tuples = [(1, 3), (2, 1), (3, 2)]
sorted_tuples = sorted(tuples, key=lambda x: x[1])
print(sorted_tuples)

# Example 4: Sort numbers descending
nums = [4, 1, 7, 3]
sorted_desc = sorted(nums, reverse=True)
print(sorted_desc)

# Example 5: Sort strings ignoring case
words = ["banana", "Apple", "cherry"]
sorted_case = sorted(words, key=lambda x: x.lower())
print(sorted_case)
