# Example 1: __init__ with one attribute
class Car:
    def __init__(self, brand):
        self.brand = brand
my_car = Car("Toyota")
print(my_car.brand)

# Example 2: __init__ with two attributes
class Car:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year
my_car = Car("Honda", 2020)
print(my_car.brand, my_car.year)

# Example 3: Default value in __init__
class Car:
    def __init__(self, brand, year=2023):
        self.brand = brand
        self.year = year
my_car = Car("Ford")
print(my_car.brand, my_car.year)

# Example 4: __init__ calling method
class Car:
    def __init__(self, brand):
        self.brand = brand
        self.start()
    def start(self):
        print(f"{self.brand} is starting")
my_car = Car("Tesla")

# Example 5: Using self in __init__
class Car:
    def __init__(self, brand):
        self.brand = brand
        self.description = f"This car is a {self.brand}"
my_car = Car("BMW")
print(my_car.description)
