class Triangle:
    """
        Force keyword only argument
    """
    def __init__(self, *,  base=0, height=0):
        self.base = base
        self.height = height

    def area(self):
        return (self.base * self.height) / 2


class Square:
    """
    Force keyword only argument
    """
    def __init__(self, *, side=0):
        self.side = side

    def area(self):
        return self.side ** 2


class Rectangle:
    """
       Force keyword only argument
       """
    def __init__(self, *, height=0, length=0):
        self.height = height
        self.length = length

    def area(self):

        return self.length * self.height


class Shape:

    def __new__(cls, sides, **kwargs):
        """
        Use new to control how to create new instances; this is useful creating abstraction and different classes
        """
        if sides == 3:
            return Triangle(**kwargs)
        elif len(kwargs) == 2:
            return Rectangle(**kwargs)
        else:
            return Square(**kwargs)


if __name__ == '__main__':

    a = Shape(3, height=2, base=12,)  # triangle
    b = Shape(4, side=2,)     # square
    c = Shape(4, height=5, length=4)   # rectangle
    print(str(a.__class__))
    print(a.area())
    print(str(b.__class__))
    print(b.area())
    print(str(c.__class__))
    print(c.area())

