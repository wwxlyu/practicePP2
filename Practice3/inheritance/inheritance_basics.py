# Example 1: Simple single inheritance
class Animal:
    def speak(self):
        print("Some sound")
class Dog(Animal):
    pass
dog = Dog()
dog.speak()

# Example 2: Child overrides parent method
class Animal:
    def speak(self):
        print("Some sound")
class Cat(Animal):
    def speak(self):
        print("Meow")
cat = Cat()
cat.speak()

# Example 3: Parent with attribute
class Animal:
    def __init__(self, species):
        self.species = species
class Dog(Animal):
    pass
dog = Dog("Canine")
print(dog.species)

# Example 4: Child adds new method
class Animal:
    def speak(self):
        print("Sound")
class Dog(Animal):
    def bark(self):
        print("Woof")
dog = Dog()
dog.bark()
dog.speak()

# Examp
