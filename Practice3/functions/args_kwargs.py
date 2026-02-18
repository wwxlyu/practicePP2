# Example 1: *args for variable arguments
def sum_all(*numbers):
    return sum(numbers)
print(sum_all(1, 2, 3, 4))

# Example 2: **kwargs for keyword arguments
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")
print_info(name="Alice", age=25, city="Paris")

# Example 3: Mixing *args and **kwargs
def order_summary(customer, *items, **details):
    print(f"Customer: {customer}")
    print(f"Items: {items}")
    print(f"Details: {details}")
order_summary("Bob", "Apple", "Banana", payment="Credit Card", delivery="Yes")

# Example 4: *args in loops
def multiply_all(*nums):
    result = 1
    for n in nums:
        result *= n
    return result
print(multiply_all(2, 3, 4))

# Example 5: **kwargs with default values
def greet(**kwargs):
    name = kwargs.get("name", "Guest")
    city = kwargs.get("city", "Unknown")
    print(f"Hello {name} from {city}")
greet(name="Anna")
