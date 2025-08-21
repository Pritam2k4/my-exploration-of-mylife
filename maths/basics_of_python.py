# =====================
# Python Notes for DSA + OOP + Loops + Data Structures
# =====================

# ---------------------
# INPUT / OUTPUT
# ---------------------
# Single input
n = input("Enter a number: ")  

# Multiple inputs in one line
a, b = map(int, input().split())  

# List of integers
arr = list(map(int, input().split()))  

print("Answer:", a + b)

# ---------------------
# LOOPS
# ---------------------
for i in range(5):
    print("For Loop:", i)

for i in range(2, 11, 2):
    print("Custom Range:", i)

i = 0
while i < 5:
    print("While Loop:", i)
    i += 1

for i in range(10):
    if i == 3:
        continue
    if i == 7:
        break
    print("Loop Control:", i)

# ---------------------
# CONDITIONALS
# ---------------------
x = 10
if x > 5:
    print("Greater")
elif x == 5:
    print("Equal")
else:
    print("Smaller")

# ---------------------
# LISTS
# ---------------------
arr = [1, 2, 3, 4]
arr.append(5)
arr.pop()
arr.remove(2)
print(len(arr))
print(arr[0], arr[-1], arr[1:3])

for num in arr:
    print("List Traversal:", num)

# ---------------------
# STRINGS
# ---------------------
s = "hello"
print(len(s), s[0], s[-1], s[1:4], s.upper(), s[::-1])
if s == s[::-1]:
    print("Palindrome")

# ---------------------
# SETS
# ---------------------
s = {1, 2, 3}
s.add(4)
s.remove(2)
print(3 in s)

# ---------------------
# DICTIONARIES (HASHMAP)
# ---------------------
freq = {"a": 1, "b": 2}
freq["c"] = 3
print(freq["a"])
for k, v in freq.items():
    print(k, v)

arr = [1, 2, 2, 3, 3, 3]
freq = {}
for num in arr:
    freq[num] = freq.get(num, 0) + 1
print("Frequency:", freq)

# ---------------------
# FUNCTIONS
# ---------------------
def add(a, b):
    return a + b

print(add(2, 3))

# ---------------------
# SORTING
# ---------------------
arr = [5, 1, 4, 2]
arr.sort()
print("Ascending:", arr)
arr.sort(reverse=True)
print("Descending:", arr)

# ---------------------
# LIST COMPREHENSIONS
# ---------------------
squares = [i*i for i in range(5)]
print(squares)
evens = [x for x in range(10) if x % 2 == 0]
print(evens)

# ---------------------
# COMMON UTILITIES
# ---------------------
arr = [1, 5, 2, 9]
print(max(arr), min(arr), sum(arr))
print(arr.index(5), arr.count(2))

# ---------------------
# STACK & QUEUE
# ---------------------
stack = []
stack.append(1)
stack.append(2)
print("Stack Pop:", stack.pop())

from collections import deque
queue = deque([1, 2, 3])
queue.append(4)
print("Queue Popleft:", queue.popleft())

# ---------------------
# MATH HELPERS
# ---------------------
import math
print(math.sqrt(16), math.gcd(12, 15), math.factorial(5))

# ---------------------
# OOP BASICS
# ---------------------
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def show(self):
        print("Car:", self.brand, self.model)

car1 = Car("Tesla", "Model S")
car2 = Car("Toyota", "Corolla")
car1.show()
car2.show()

# Encapsulation
class Account:
    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amt):
        self.__balance += amt

    def get_balance(self):
        return self.__balance

acc = Account(1000)
acc.deposit(500)
print("Balance:", acc.get_balance())

# Inheritance
class Animal:
    def speak(self):
        print("This animal makes a sound")

class Dog(Animal):
    def speak(self):
        print("Woof!")

class Cat(Animal):
    def speak(self):
        print("Meow!")

Dog().speak()
Cat().speak()

# Polymorphism
for animal in (Dog(), Cat()):
    animal.speak()

# Abstraction
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14 * self.r * self.r

print("Circle Area:", Circle(5).area())

# Static & Class methods
class Demo:
    @staticmethod
    def static_method():
        print("Static method")
    @classmethod
    def class_method(cls):
        print("Class method", cls)

Demo.static_method()
Demo.class_method()

# Operator overloading
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

p1, p2 = Point(1, 2), Point(3, 4)
p3 = p1 + p2
print("Point Sum:", p3.x, p3.y)

# Destructor
class Example:
    def __init__(self):
        print("Object created")
    def __del__(self):
        print("Object destroyed")

obj = Example()
del obj
