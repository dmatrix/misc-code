""""
Another simple example from medium that illustrates the difference
between threads and processes, and also how to get around GIL
https://medium.com/towards-artificial-intelligence/the-why-when-and-how-of-using-python-multi-threading-and-multi-processing-afd1b8a8ecca
"""
import multiprocessing as mp
import concurrent.futures as mt
import time


def get_cpu_count():
    return mp.cpu_count()


def is_prime(n):
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def compute_primes(n):
    return [n for n in range(num) if is_prime(n)]


if __name__ == '__main__':

    # A CPU bound task
    num = 1000000
    start = time.time()
    prime_numbers = [n for n in range(num) if is_prime(n)]
    end = time.time()
    print(f"Serial access: Time elapsed: {end - start:4.2f} sec to compute all primes in {num} are {len(prime_numbers)} ")

    # A multi-threaded approach for CPU bound task
    start = time.time()
    with mt.ThreadPoolExecutor(get_cpu_count()) as executor:
        prime_numbers = executor.map(is_prime, list(range(num)))
    end = time.time()
    print(f"Multi-threaded access: Time elapsed: {end - start:4.2f} sec to compute all primes in {num} are {sum(list(prime_numbers))}")

    # Let's try multiprocess for each core
    # Since this is CPU I/O bound task, we should get better performance
    # the serial and threading
    #
    start = time.time()
    with mp.Pool(get_cpu_count()) as p:
        prime_numbers = p.map(is_prime, list(range(num)))
    end = time.time()
    print(f"Multi-process access: Time elapsed: {end - start:4.2f} sec to compute all primes in {num} are {sum(list(prime_numbers))}")
