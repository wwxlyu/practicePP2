words = ["a", "b", "c"]

for i, word in enumerate(words):
    print(i, word)

nums = [1, 2, 3]
letters = ["a", "b", "c"]

for n, l in zip(nums, letters):
    print(n, l)