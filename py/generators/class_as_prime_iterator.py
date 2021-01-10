"""
Generator functions allows you to create functions that act as iterators,
An iterator is an object that can be iterated (looped) upon. It implements
the iterator protocal by implementing __next__ and __iter__ methods.

Also, iterators save memory space as they lazily evaluate or process the
next item, only when __next__ is invoked.

They only compute it when you ask for it. This is known as lazy evaluation.

source: https://medium.com/free-code-camp/how-and-why-you-should-use-python-generators-f6fb56650888
"""


def _is_prime(n):
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


class Primes:

    def __init__(self, maximum):
        """
        Compute all prime numbers that are smaller than a maximum number.
        Parameters
        ----------
            int
                Compute all prime numbers that are smaller than a maximum number
        """
        self.max = maximum
        self.number = 1

    def __iter__(self):
        """
        Implements iter as part of the Iterator protocol

        Returns
        -------
            cls: class
                Always returns itself

       """
        return self

    def __next__(self):
        self.number += 1
        if self.number >= self.max:
            raise StopIteration
        elif _is_prime(self.number):
            return self.number
        else:
            return self.__next__()


if __name__ == '__main__':

    # Nothing is computed  here at class initialization
    primes = Primes(15)

    # Now primes as an object can be used as an iterator object in a look
    # the numbers are lazily evaluated
    for prime in primes:
        print(prime)

