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

    NUM_TASKS = [25, 50, 75, 100]
    for task in NUM_TASKS:
        obj_ref = [ray_task.remote(random.randint(100, 200), random.randint(100, 200)) for i in range(task)]
        print("Num of tasks: {task}")
        results = sum(ray.get(object_refs=obj_ref))
        print(f"Number of arrays: {len(obj_ref)}, Sum of all Numpy arrays: {results:.2f})")
