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
        return self.length ** 2


class Rectangle:
    def __init__(self, height, length):
        self.height = height
        self.length = length

    def area(self):

        return self.length * self.height


class Shape:

    def __new__(cls, sides, *args, **kwargs):
        """
        Use new to control how to create new instances; this is useful creating abstraction and different classes
        """
        if sides == 3:
            return Triangle(*args, **kwargs)
        elif len(args) == 2 or len(kwargs) == 2:
            return Rectangle(*args, **kwargs)
        else:
            return Square(*args, **kwargs)


if __name__ == '__main__':

    a = Shape(3, 2, 12)  # triangle
    b = Shape(4, 2,)     # square
    c = Shape(4, height=5, length=4)   # rectangle
    print(str(a.__class__))
    print(a.area())
    print(str(b.__class__))
    print(b.area())
    print(str(c.__class__))
    print(c.area())

