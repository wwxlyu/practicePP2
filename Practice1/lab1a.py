#1 Data types
x = 35e3
y = 12E4
z = -87.7e100

print(type(x))
print(type(y))
print(type(z))

#2
x = 1    # int
y = 2.8  # float
z = 1j   # complex

#convert from int to float:
a = float(x)

#convert from float to int:
b = int(y)

#convert from int to complex:
c = complex(x)

print(a)
print(b)
print(c)

print(type(a))
print(type(b))
print(type(c))

#3
a = "Hello, World!" #otput 1 index
print(a[1])


#4
a = "Let's make it better!"
print(len(a))


#5
txt = "I would like to have more free time!"
print("free" in txt)