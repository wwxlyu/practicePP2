# Example 1: Positional arguments
def introduce(name, age):
    print(f"My name is {name}, and I am {age} years old.")
introduce("Alice", 20)

# Example 2: Keyword arguments
def info(name, city):
    print(f"{name} lives in {city}.")
info(city="London", name="Bob")

# Example 3: Default arguments
def greet_user(name="Guest"):
    print(f"Hello, {name}!")
greet_user()
greet_user("Anna")

# Example 4: Mixing positional and keyword arguments
def describe_pet(pet_name, animal_type="dog"):
    print(f"I have a {animal_type} named {pet_name}.")
describe_pet("Buddy")
describe_pet("Whiskers", animal_type="cat")

# Example 5: Function with multiple arguments
def calculate_total(price, quantity, tax=0.05):
    total = price * quantity * (1 + tax)
    return total
print(calculate_total(100, 2))
