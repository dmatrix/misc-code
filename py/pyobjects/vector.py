from array import array
import reprlib
import math
import numbers

# A Python class to illustrate a User-defined Sequence Type

class Vector:
   typecode = 'd'
   short_names = 'xyzt'

   def __init__(self, components):
      '''
      Constructor
      '''
      # Proctected components that holds array with Vector components
      self._components = array(self.typecode, components)

   def __iter__(self):
      '''
      Make this an iterable
      '''
      return iter(self._components)

   def __repr__(self):
      '''
      Use reprlib.repr() to get a limited-length representation of self._components
      '''
      components = reprlib.repr(self._components)
      # Remove array('d', prefix and trailing ')'
      components = components[components.find('['), :-1]
      return (f"Vector({components})")

   def __str__(self):
      return str(tuple(self))

   def __bytes__(self):
      return (bytes([ord(self.typecode)]) + bytes(self._components))

   def __eq__(self, other):
      return tuple(self) == tuple(other)

   def __abs__(self):
      return math.sqrt(sum(x *x for x in self))

   def __len__(self):
      return len(self._components)

   def __getitem__(self, index):
      # Get the class of the instace (i.e., Vector)
      cls = type(self)
      # check in the index is of type slice
      if isinstance(index, slice):
         # Delegate the to create another instance of class with slice
         return cls(self._components[index])
      elif isinstance(index, numbers.Integral):
         return self._components[index]
      else:
         # Raise exception
         msg = "{cls.__name__} indices must be integers or slices"
         raise TypeError(msg.format(cls=cls))

   def __getattr__(self, name):
      cls = type(self)
      if len(name) == 1:
         # one of the shortname characters
         pos = cls.short_names.find(name)
         # is position within range
         if 0 <= pos < len(self._components):
            return self._components[pos]
      msg = '{._name__!r} object has no attribute {!r}'
      raise AttributeError(msg.format(cls, name))

   def __setattr__(self, name, value):
      cls = type(self)
      if len(name) == 1:
         if name in cls.short_names:
            error = 'readonly attribute {attr_name!r}'
         elif name.islower():
            error = "cant't se attributes 'a' to 'z' in {cls_name!r}"
         else:
            error = ''
         if error:
            msg = error.format(cls_name=cls.__name__, attr_name=name)
            raise AttributeError(msg)
      super().__setattr__(name, value)

   @classmethod
   def frombytes(cls, octets):
      typecode = chr(octets[0])
      memv = memoryview(octets[1:]).cast(typecode)
      return cls(memv)

if __name__ == "__main__":

   v = Vector([3, 4, 5])
   print(len(v))

   v7 = Vector(range(7))
   print(v7)

   print(v7[-1])
   print(v7[1:4])
   print(v7[-1:])
   print(v7.x)
   print(v7.t)

   v7.f = 5
