import re
import reprlib
from typing import Pattern

RE_WORD: Pattern[str] = re.compile("\w+")


class GenSentence:
    def __init__(self, text):
        # No need to have a words list
        self.text = text

    def __repr__(self):
        return 'LazySentence(%s' % reprlib.repr(self.text)

    def __iter__(self):
        # build a generator expression over matches on RE_WORD on self.text, yielding generator expression
        return (match.group() for match in RE_WORD.finditer(self.text))


if __name__ == '__main__':
    s = GenSentence('"The time has come," the Walrus said,')
    print(s)
    for w in s:
        print(w)
