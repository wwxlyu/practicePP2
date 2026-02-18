# Example 1: Using super() to call parent __init__
class Animal:
    def __init__(self, species):
        self.species = species
class Dog(Animal):
    def __init__(self, name, species):
        super().__init__(species)
        self.name = name
dog = Dog("Buddy", "Canine")
print(dog.name, dog.species)

# Example 2: Calling parent method
class Animal:
    def speak(self):
        print("Animal sound")
class Cat(Animal):
    def speak(self):
        super().speak()
        print("Meow")
c = Cat()
c.speak()

# Example 3: super() with multiple inheritance
