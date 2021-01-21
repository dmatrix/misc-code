import sys
from abc import ABCMeta, abstractmethod
import logging


class Shape:

    __metaclass__ = ABCMeta

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)

    @abstractmethod
    def area(self, **kwargs):
        pass


class Triangle(Shape):
    def __init__(self, *, base=0, height=0):
        super(Triangle, self).__init__()
        self._base = base
        self._height = height

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, value):
        self._base = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def area(self):
        return (self._base * self._height) / 2


class Square(Shape):
    def __init__(self, *, side=0):
        super(Square, self).__init__()
        self.side = side

    def area(self):
        return self.side ** 2


class Rectangle(Shape):
    def __init__(self, *, length=0, height=0):
        super(Rectangle, self).__init__()
        self.length = length
        self.height = height

    def area(self):
        return self.length * self.height


if __name__ == '__main__':
    a = Triangle(height=2, base=12, )  # triangle
    b = Square(side=4)  # square
    c = Rectangle(height=5, length=4)  # rectangle
    print(str(a.__class__))
    print(a.area())
    print("--" * 4)
    # set new property for triangle
    a.height = 4
    a.base = 4
    print(str(a.__class__))
    print(a.area())
    print(str(b.__class__))
    print(b.area())
    print(str(c.__class__))
    print(c.area())
    print(__name__)
    for cls in [a, b, c]:
        print('{} class variables: {}'.format(cls.__class__.__name__, vars(cls)))

    print(sys.modules)

