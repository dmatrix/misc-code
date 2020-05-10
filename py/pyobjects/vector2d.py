from array import array
import math
class Vector2D:
   # class wide attribute to convert this instances into bytes
   typecode = 'd'

   def __init__(self, x, y):
      """
      Constructor for the class
      """
      self.__x = float(x)
      self.__y = float(y)

   @property
   def x(self):
      return self.__x

   @property
   def y(self):
      return self.__y

   def __iter__(self):
      """
      Make this class iterable by using generator expression
      """
      return (i for i in (self.x, self.y))

   def __repr__(self):
      """
      build a interoperable string by using {!r} to get their repr
      """
      class_name = type(self).__name__
      return '{}({!r}, {!r})'.format(class_name, *self)

   def __str__(self):
      """
      Build an order pair for printing
      """
      return str(tuple(self))

   def __bytes__(self):
      """
      Generate bytes
      """
      return (bytes([ord(self.typecode)]) +
              bytes(array(self.typecode, self)))

   def __hash__(self):
      return hash(self.x) ^ hash(self.y)

   def __eq__(self, other):
      return tuple(self) == tuple(other)

   def __abs__(self):
      return math.hypot(self.x, self.y)

   def __boolean__(self):
      return bool(abs(self))

   def __format__(self, fmt_spec=''):
      components = (format(c, fmt_spec) for c in self)
      return ('({}, {})'.format(*components))

   @classmethod
   def frombytes(cls, octets):
      """
      alternative class constructor
      """
      # get the typecode encoded in the first character
      tc = octets[0]
      memv = memoryview(octets[1:]).cast(tc)
      return cls(*memv)

if __name__ == "__main__":
   v1 = Vector2D(3, 4)
   print(v1)
   print(v1.x, v1.y)
   x, y = v1
   print(x, y)

   v1_clone = eval(repr(v1))
   print(v1 == v1_clone)
   octets = bytes(v1)
   octets_2 = bytes(v1_clone)
   print(octets)
   print(octets)
   print(abs(v1))
   print(bool(v1), bool(Vector2D(0,0)))

   vf = Vector2D(3, 4)
   print(format(vf))
   print(format(vf, '.2f'))
   print(format(vf, '.3e'))

   vh_1 = Vector2D(3,4)
   vh_2 = Vector2D(3.1, 4.2)
   print((hash(vh_1), hash(vh_2)))
   print(set([vh_1, vh_2]))
