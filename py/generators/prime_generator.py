"""
Generator functions allow you create simple iterators.
These functions use yield statement to produce or generate
the next computed value, and suspend, saving the current
state of the function.

source: https://medium.com/free-code-camp/how-and-why-you-should-use-python-generators-f6fb56650888

Summary:

1. Use generators to create iterators in a pythonic way
2. Iterators allow lazy evaluation, by only generating the next element of an iterable object
   when requested. This is useful for very large data sets.
3. Iterators and generators, once inialized, can only be used once.
4. Generally, generator functions are better than iterators
5. For simple cases, generator expressions are better than iterators

"""


def _is_prime(n):
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def gen_primes(maximum):
    number = 1

    # Loop forever
    while number <= maximum:
        number += 1
        if _is_prime(number):
            yield number


if __name__ == '__main__':
    primes = gen_primes(25)
    print(primes)
    # Use the generator now as an iterator
    for prime in primes:
        print(prime)

    print("--" * 5)

    # Use it as a generator
    primes = gen_primes(25)
    while True:
        try:
            prime = next(primes)
            print(prime)
        except StopIteration as ex:
            break
    print("--" * 5)

    # Use it as a generator expression
    primes = (p for p in range(2, 25) if _is_prime(p))
    for prime in primes:
        print(prime)

    print("--" * 5)

    # Use it as a generator in a list comp
    primes = [p for p in range(2, 25) if _is_prime(p)]
    for prime in primes:
        print(prime)
