""""
Another simple example from medium that illustrates the difference
between threads and processes, and also how to get around GIL
https://medium.com/towards-artificial-intelligence/the-why-when-and-how-of-using-python-multi-threading-and-multi-processing-afd1b8a8ecca
"""
import concurrent.futures as mt
import multiprocessing as mp
import time
import ray
from ray.util.multiprocessing import Pool
from defs import is_prime, get_cpu_count


if __name__ == '__main__':

    # A CPU bound task
    num = 2000000
    start = time.time()
    prime_numbers = [n for n in range(num) if is_prime(n)]
    end = time.time()
    print(f"Serial access: Time elapsed: {end - start:4.2f} sec to compute all primes in {num} are {len(prime_numbers)} ")

    # A multi-threaded approach for CPU bound task
    start = time.time()
    with mt.ThreadPoolExecutor(get_cpu_count()) as executor:
        prime_numbers = executor.map(is_prime, list(range(num)))
    end = time.time()
    print(f"Multi Threaded access: Time elapsed: {end - start:4.2f} sec to compute all primes in {num} are {sum(list(prime_numbers))}")

    # Let's try multiprocess for each core
    # Since this is CPU I/O bound task, we should get better performance
    # the serial and threading
    #
    start = time.time()
    mp_pool = mp.Pool(get_cpu_count())
    with mp_pool as p:
        prime_numbers = p.map(is_prime, list(range(num)))
    end = time.time()
    mp_pool.terminate()

    print(f"Multi Process access: Time elapsed: {end - start:4.2f} sec to compute all primes in {num} are {sum(list(prime_numbers))}")

    # Let's try that with Ray multiprocessing pool
    ray.init()
    ray_pool = Pool(get_cpu_count())
    lst = list(range(num))
    results = []
    start = time.time()
    for result in ray_pool.map(is_prime, lst):
        results.append(result)
    end = time.time()
    ray_pool.terminate()
    print(f"Ray Distributed Multi Process access: Time elapsed: {end - start:4.2f} sec to compute all primes in {num} are {sum(results)}")
    ray.shutdown()

