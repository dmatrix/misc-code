import random

from tombola import Tombola


class BingoCage(Tombola):

   def __init__(self, items):
      super(BingoCage, self).__init__()
      self._randomizer = random.SystemRandom()
      self._items = []
      self.load(items)

   def __repr__(self):
      s = f'<BingoCage({self._items})>'
      return s

   def load(self, items):
      self._items.extend(items)
      self._randomizer.shuffle(self._items)

   def pick(self):
      try:
         return self._items.pop()
      except IndexError:
         raise LookupError('pick from empty BingoCage')

   def __call__(self):
      self.pick()


if __name__ == '__main__':

   b = BingoCage([1, 2, 3])
   print(b)
