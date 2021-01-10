import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence({})'.format(reprlib.repr(self.text))

    def __iter__(self):
        """
        implements the iterator protocol and generator using yield
        """
        for word in self.words:
            yield word
        return


if __name__ == '__main__':
    s = Sentence("This is a cool example of how iterators and generators are implemented")
    for w in s:
        print(w)
    print(s)
    print(type(s))
