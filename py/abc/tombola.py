import abc
from abc import ABC


class Tombola(ABC):
   """
   Define an ABC subclass
   """
   @abc.abstractmethod
   def load(self, iterable):
      """Add items from the iterator"""

   @abc.abstractmethod
   def pick(self):
      """Remove item at random, returning it
      This method should raise `LookupError` when the instance is empty
      """
   def loaded(self):
      """Retrun `True` if there's at least i item, 'Falss` otherwise"""
      return bool(self.inspect())

   def inspect(self):
      """Return a sorted tuple with the items currently inside"""
      items = []
      while True:
         try:
            items.append(self.pick())
         except LookupError:
            break
      self.load(items)
      return sorted(items)

if __name__ == '__main__':
   fake = Tombola()
