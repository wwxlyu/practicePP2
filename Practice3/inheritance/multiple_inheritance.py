# Example 1: Simple multiple inheritance
class A:
    def greet(self):
        print("Hello from A")
class B:
    def greet(self):
        print("Hello from B")
class C(A, B):
    pass
c = C()
c.greet()  # Uses method from first parent (A)

# Example 2: Child defines own method
class A:
    def greet(self):
        print("Hello from A")
class B:
    def greet(self):
        print("Hello from B")
class C(A, B):
    def greet(self):
        print("Hello from C")
c = C()
c.greet()

# Example 3: Access parent methods explicitly
class A:
    def greet(self):
        print("A says hi")
class B:
    def greet(self):
        print("B says hi")
class C(A, B):
    def greet(self):
        A.greet(self)
        B.greet(self)
c = C()
c.greet()

# Example 4: Multiple inheritance with __init__
class A:
    def __init__(self):
        print("Init A")
class B:
    def __init__(self):
        print("Init B")
class C(A, B):
    def __init__(self):
        super().__init__()
c = C()  # Only calls A due to MRO

# Example 5: Multiple inheritance with attributes
class A:
    x = 10
class B:
    y = 20
class C(A, B):
    pass
c = C()
print(c.x, c.y)
