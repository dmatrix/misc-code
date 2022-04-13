import numpy as np
import ray


@ray.remote
def random():
    # Create random array of 10 numbers with huge value
    return np.random.randint(0, 11,
                             10 ** 8 // 8) # 100MB


@ray.remote
def mean(array):
    return array.mean()


if __name__ == "__main__":

    # Set the memory limit to 10 GB
    # Allow up to store 10 arrays of
    ray.init(object_store_memory=10 ** 9)

    # Generate 20 arrays in parallel in a comprehension list
    # this may produce on OOM error
    means = [ray.get(random.remote()) for _ in range(100)]
    arrays = [random.remote() for _ in range(20)]

    print(f"Means: {np.mean(means)}")