from random import randrange
from tombola import Tombola

#
# Register as a virtual sublclass of Tombola
#
@Tombola.register
class TomboList(list):
   """Extends as the sublcass of list"""

   def pick(self):
      # TomboList inherits bool from list
      # returns True if not empty
      if self:
         position = randrange(len(self))
         # use inherited pop() from the list
         return self.pop(position)
      else:
         # list is empty
         raise LookupError('pop from an empty list')

   load = list.extend

   def loaded(self):
      return bool(self)

   def inspect(self):
      return tuple(sorted(self))

if __name__ == '__main__':
   tl = TomboList(list(range(10)))
   print(issubclass(TomboList, Tombola))
   print(isinstance(tl, TomboList))
   print(isinstance(tl, Tombola))
   print(TomboList.__mro__)
