class Shape:
    def __new__(cls, sides, *args, **kwargs):
        if sides == 3:
            return Triangle(*args, **kwargs)
        else:
            return Square(*args, **kwargs)
 
 
class Triangle:
    def __init__(self, base, height):
        self.base = base
        self.height = height
 
    def area(self):
        return (self.base * self.height) / 2
 
 
class Square:
    def __init__(self, length):
        self.length = length
 
    def area(self):
        return self.length*self.length
 
 
a = Shape(sides=3, base=2, height=12)
b = Shape(sides=4, length=2)
 
print(str(a.__class__))
print(a.area())
 
print(str(b.__class__))
print(b.area())
 