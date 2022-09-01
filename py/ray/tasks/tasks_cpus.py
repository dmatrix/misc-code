import os
import time
import math
import ray
import numpy as np
import random
import logging

@ray.remote
def ray_task(a, b):
    arr = np.random.rand(a,b)
    return math.sqrt(np.sum(arr)) * a * b

if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    obj_ref = [ray_task.remote(random.randint(10000, 50000), random.randint(10000, 50000)) for i in range(100)]
    results = sum(ray.get(object_refs=obj_ref))
    print(f"Number of arrays: {len(obj_ref)}, Sum of all Numpy arrays: {results:.2f})")
    ra