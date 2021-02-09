"""
Meta classes is a way to write code to modify the behavior of a class's method, attributes or
functions. It's as though you are decorating its methods or adding new functionality dynamically,
allowing you to extend or reduce its functionality and alter its behavior dynamically.

Let's look a short example from:
source: https://medium.com/better-programming/meta-programming-in-python-7fb94c8c7152
"""
from utils_decorators import debug_all_methods


class MetaClassDebug(type):
    # Create a new instance here
    def __new__(cls, clsname, bases, clsdict):
        obj = super().__new__(cls, clsname, bases, clsdict)

        # All the methods for this new instance are decorated or modified
        obj = debug_all_methods(obj)
        return obj


class Calc(metaclass=MetaClassDebug):
    def add(self, x, y):
        return x + y

    def sub(self, x, y):
        return x - y

    def mul(self, x, y):
        return x * y

    def div(self, x, y):
        return x / y


if __name__ == '__main__':
    calc = Calc()
    print(calc.add(4, 2))
    print(calc.sub(4, 2))
    print(calc.mul(4, 2))
    print(calc.div(4, 2))

