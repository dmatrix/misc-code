#
# source: https://medium.com/techtofreedom/iterable-and-iterator-in-python-dbe7011d1ff7
#
# Class hierarchy
#
#  Generator --> Iterator --> Iterable
#
# Some key concepts to distinguish between iterator and iterable
# Iterables
# ---------
#  1. Collections or containers such as list, set, tuple, dictionary are iterables
#     That is, the contain or hold all elements in the container. And as such, they
#     can be part of the for x.. in collection: loop
#  2. Any object that can be used in the for .. in loop is an iterable
#
# Iterators
# ---------
#  1. Iterator is a subclass of Iterable
#  2. Iterator does not contain all elements but can produce an element when
#     requested through the `next`() call
#  3. Iterator can be created from an iterable via it = iter(iterable_object)
#  4. Each element can then be fetched as need via elem = next(it)
#  5. Or it could be used as for e in it:
#  6. Any Python object can be made into an Iterator by implementing two methods:
#      a. __iter__() an initializes an iterator and returns an object that has the __next__() method.
#      b. __next__() returns produces the next element.
#
# Generators
# -----------
#  1. Generators can be used as Iterators, whereby you don't have to implement
#     __iter_() or __next()__ method each time you need an object to be used
#     as an iterator
#
# Summary:
# --------
# In a word, an Iterable object in Python is an object that can be iterated (by for loop).
# Iterator is subclass of Iterable but it contains an item producing next() method rather than items.

from collections.abc import Iterable, Iterator


class Fib(object):
    """
    Class the implements a Fibonacci sequence
    """
    def __init__(self, stop=100):
        """
        Constructor to initialize the series

        Parameters
        ----------
        stop: int
            stop the series at, default 100
        """
        self.a, self.b = 0, 1
        self.stop = stop

    def __iter__(self):
        """
        Implement the iterable method as part of the Iterator protocol class

        Returns
        -------
            self
        """
        return self

    def __next__(self):
        """
        Implements the __next__() method to generate the next element in the series
        and stops by raising an exception when limit is reached
        """
        self.a, self.b = self.b, self.a + self.b
        if self.a > self.stop:
            raise StopIteration

        return self.a


def fib_gen(stop=100):
    """
    Implements a generator.

    Parameters
    ----------
    stop: int
        Stop generating when reached this limit, default is 100
    """

    n, a, b = 0, 0, 1
    while (n < stop):
        yield b
        a, b, = b, a + b
        n += 1
    return 'done'


if __name__ == '__main__':

    # create an iterable list
    my_list = [1, 2, 3, 4]

    # create an iterator from the list
    my_iter = iter(my_list)

    print(type(my_list))
    print(isinstance(my_list, Iterable))
    print(type(my_iter))
    print(isinstance(my_iter, Iterator))
    print(isinstance(my_iter, Iterable))
    print(isinstance(my_list, Iterator))

    # Use in the loop
    print('Using an iterable to iterate my_list')
    for e in my_list:
        print(e)
    print('Using an iterator to iterate my_list')
    for e in my_iter:
        print(e)
    my_iter = iter([8, 9])
    print('Using an iterator to fetch an element with next()')
    print(next(my_iter))
    print(next(my_iter))

    # Use the Fib as an iterator and iterable
    print('Using Fib class as an iterator')
    f = Fib(stop=10)
    for n in iter(f):
        print(n)
    print('Using Fib class as an iterator using next()')
    f = Fib(stop=10)
    print(next(f))
    print(next(f))
    print(next(f))
    print(next(f))
    print('Using gen_fib function as an generator using next()')
    f = fib_gen(stop=10)
    print(next(f))
    print(next(f))
    print(next(f))
    print(next(f))


