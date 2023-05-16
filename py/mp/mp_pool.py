import multiprocessing as mp
from ray.util.multiprocessing import Pool
import ray
import numpy as np
import os
import time
import logging
from defs import get_cpu_count

# iterations_count = round(1e7)
iterations_count = round(1e5)

def f(x):
    pid = os.getpid()
    ppid = os.getppid()
    res = x ** 2
    print(f"Parent pid: {ppid}, Child pid: {pid}, res :{res}")
    return res

def inefficient_fib(n=None):
    """Compute intensive calculation for the nth fibonacci number"""
    if n <= 1:
        return n
    return inefficient_fib(n - 1) + inefficient_fib(n - 2)

def is_prime(n):
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return 0
    return 1


def complex_operation_numpy(index):
   data = np.ones(iterations_count)
   val = np.exp(data) * np.sinh(data)
   return val.sum()

if __name__ == '__main__':
    cores = mp.cpu_count()
    print(f"number of cores: {cores}")
    start = time.time()
    mp_pool = mp.Pool(cores)
    with mp_pool as p:
        results = p.map(is_prime, list(range(200000)))
    print(f"sum of all: {sum(results):.2f}")
    end = time.time()
    mp_pool.terminate()
    print(f"Multi Process access: Time elapsed: {end - start:.2f} sec")


    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    results = []
    ray_pool = Pool(get_cpu_count())
    start = time.time()
    for result in ray_pool.map(is_prime, list(range(2000000))):
        results.append(result)
    end = time.time()
    print(f"sum of all: {sum(results):10.2f}")
    print(f"Ray Multi Process access: Time elapsed: {end - start:10.2f} sec")
    ray.shutdown()



    
