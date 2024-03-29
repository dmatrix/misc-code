import multiprocessing as mp
import numpy as np

# iterations_count = round(1e7)
iterations_count = round(1e5)

def complex_operation_numpy(index):
   data = np.ones(iterations_count)
   val = np.exp(data) * np.sinh(data)
   return val.sum()

def get_cpu_count():
    return mp.cpu_count()


def inefficient_fib(n=33):
    """Compute intensive calculation for the nth fibonacci number"""
    if n <= 1:
        return n
    return inefficient_fib(n - 1) + inefficient_fib(n - 2)
    
def is_prime(n):
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return 0
    return 1



