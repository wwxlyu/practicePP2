#map() filter()
nums = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, nums))
even = list(filter(lambda x: x % 2 == 0, nums))
print(squared)
print(even)

#reduce() combining all elements into one value
from functools import reduce #functools for escape loops
nums = [1, 2, 3, 4]
total = reduce(lambda x, y: x + y, nums)
print(total)


#check types
x = "123"
print(type(x))

#transforming into int etc
num = int(x)