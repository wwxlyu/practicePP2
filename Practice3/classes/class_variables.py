# Example 1: Class variable
class Dog:
    species = "Canine"
dog1 = Dog()
dog2 = Dog()
print(dog1.species, dog2.species)

# Example 2: Class variable accessed via class
print(Dog.species)

# Example 3: Instance variable vs class variable
class Dog:
    species = "Canine"
    def __init__(self, name):
        self.name = name
dog1 = Dog("Buddy")
dog2 = Dog("Max")
print(dog1.name, dog1.species)
print(dog2.name, dog2.species)

# Example 4: Changing class variable
Dog.species = "Dog"
print(dog1.species, dog2.species)

# Example 5: Instance can override class variable
dog1.species = "Wolf"
print(dog1.species, dog2.species)
