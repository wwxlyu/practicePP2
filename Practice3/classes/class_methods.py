# Example 1: Simple instance method
class Person:
    def greet(self):
        print("Hello!")
p = Person()
p.greet()

# Example 2: Method using attribute
class Person:
    def __init__(self, name):
        self.name = name
    def greet(self):
        print(f"Hi, my name is {self.name}")
p = Person("Alice")
p.greet()

# Example 3: Method returning a value
class Person:
    def __init__(self, age):
        self.age = age
    def is_adult(self):
        return self.age >= 18
p = Person(20)
print(p.is_adult())

# Example 4: Method changing attribute
class Person:
    def __init__(self, age):
        self.age = age
    def have_birthday(self):
        self.age += 1
p = Person(25)
p.have_birthday()
print(p.age)

# Example 5: Method calling another method
class Person:
    def __init__(self, name):
        self.name = name
    def greet(self):
        return f"Hi, {self.name}"
    def welcome(self):
        print(self.greet() + "!")
p = Person("Bob")
p.welcome()
