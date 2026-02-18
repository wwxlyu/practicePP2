# Example 1: Simple method override
class Animal:
    def sound(self):
        print("Some sound")
class Dog(Animal):
    def sound(self):
        print("Woof")
dog = Dog()
dog.sound()

# Example 2: Override and call parent method
class Animal:
    def sound(self):
        print("Some sound")
class Cat(Animal):
    def sound(self):
        print("Meow")
        super().sound()
c = Cat()
c.sound()

# Example 3: Override with attributes
class Vehicle:
    def info(self):
        print("Generic vehicle")
class Car(Vehicle):
    def info(self):
        print("Car info")
c = Car()
c.info()


# Example 4: Multi-level overriding
class A:
    def show(self):
        print("A")
class B(A):
    def show(self):
        print("B")
class C(B):
    def show(self):
        print("C")
c = C()
c.show()
