from collections.abc import *
import collections
Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck(MutableSequence):
   ranks  = [str(n) for n in range(2, 11)] + list('JQKA')
   suits = 'spades diamonds clubs hearts'.split()

   def __init__(self):
      # Create a full deck of cards
      # [Card(rank='2', suit='spades'),
      #  Card(rank='3', suit='spades')
      #  ..
      #  Card(rank='A', suit='hearts')]
      self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

   # Implements Sequence protocol
   def __len__(self):
      # should be 52 cards
      return len(self._cards)

   # Implements Sequence protocol
   def __getitem__(self, item):
      return self._cards[item]

   # Implements mutable protocol so we can suffle
   def __setitem__(self, key, value):
      self._cards[key] = value

   # Need to implement abstract class method
   def __delitem__(self, key):
      del self._cards[key]

   # Need to implement abstract class method
   def insert(self, index: int, value):
      self._cards.insert(index, value)

   @property
   def cards(self):
      return self._cards

if __name__ == '__main__':
   deck = FrenchDeck()
   print(deck.cards)
