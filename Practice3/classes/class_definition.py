# Example 1: Simple class with no methods
class Dog:
    pass
my_dog = Dog()
print(my_dog)

# Example 2: Class with one method
class Dog:
    def bark(self):
        print("Woof!")
my_dog = Dog()
my_dog.bark()

# Example 3: Class with attribute
class Dog:
    def __init__(self, name):
        self.name = name
my_dog = Dog("Buddy")
print(my_dog.name)

# Example 4: Class with default attribute
class Dog:
    def __init__(self, name="Unknown"):
        self.name = name
my_dog = Dog()
print(my_dog.name)

# Example 5: Class with multiple attributes
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
my_dog = Dog("Max", 5)
print(my_dog.name, my_dog.age)
