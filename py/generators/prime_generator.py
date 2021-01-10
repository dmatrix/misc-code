"""
Generator functions allow you create simple iterators.
These functions use yield statement to produce or generate
the next computed value, and suspend, saving the current
state of the function.
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
