import re
import reprlib
from typing import Pattern

RE_WORD: Pattern[str] = re.compile("\w+")


class Sentence:
   def __init__(self, text):
      self._text = text
      self._words = RE_WORD.findall(text)

   @property
   def text(self):
      return self._text

   @property
   def words(self):
      return self._words

   def __getitem__(self, index):
      """
      Implements a sequence protocol
      """
      return self._words[index]

   def __len__(self):
      """
      Implements as part of sequence protocol
      """
      return len(self._words)

   def __repr__(self):
      return 'Sentence(%s)' % reprlib.repr(self._text)


if __name__ == '__main__':
   s = Sentence('"The time has come," the Walrus said,')
   print(s)
   print(s.words)
   print(s[-1])
   for w in s:
      print(w)
   print(list(s))
