
import math
import random
import time
from typing import Tuple, List
import os
import ray

# Change this to match your cluster scale.
NUM_SAMPLING_TASKS = os.cpu_count()
NUM_SAMPLES_PER_TASK = 10_000_000
TOTAL_NUM_SAMPLES = NUM_SAMPLING_TASKS * NUM_SAMPLES_PER_TASK

def sampling_task(num_samples: int, task_id: int) -> int:
    num_inside = 0
    for i in range(num_samples):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        # check if the point is inside the circle
        if math.hypot(x, y) <= 1:
            num_inside += 1
    print(f"Task id: {task_id} | Samples in the circle: {num_inside}")
    return num_inside

@ray.remote
def sample_task_distribute(sample_size, i) -> object:
    return sampling_task(sample_size, i)

def run_serial(sample_size) -> List[int]:
    results = [sampling_task(sample_size, i+1) for i in range(NUM_SAMPLING_TASKS)]
    return results

def run_disributed(sample_size) -> List[int]:
    results = ray.get([
            sample_task_distribute.remote(sample_size, i+1) for i in range(NUM_SAMPLING_TASKS)
        ])
    return results


def calculate_pi(results: List[float]) -> float:
    total_num_inside = sum(results)
    pi = (total_num_inside * 4) / TOTAL_NUM_SAMPLES
    return pi


if __name__ == "__main__":
    print(f"Running {NUM_SAMPLING_TASKS} tasks serially....")
    start = time.time()
    results = run_serial(NUM_SAMPLES_PER_TASK)
    end = time.time()
    pi = calculate_pi(results)
    print(f"Estimated value of π is: {pi:5f} | estimated local time: {end-start:.2f} sec")  

    # Run remote
    print("--" * 10)
    print(f"Running {NUM_SAMPLING_TASKS} tasks distributed....")
    if  ray.is_initialized():
        ray.shutdown()
    ray.init()

    start = time.time()
    results = run_disributed(NUM_SAMPLES_PER_TASK)
    end = time.time()
    pi = calculate_pi(results)
    print(f"Estimated value of π is: {pi:5f} | estimated distributed time: {end-start:.2f} sec")  