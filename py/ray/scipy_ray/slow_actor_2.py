from typing import List
import time

import numpy
import numpy as np
import ray

# Explain the behavior of this example
# 1. Actor invoking a local task
# 2. What's the expected behavior: are tasks being executed serially?
# 3. Everything is serialized, nothing is distributed


def slow_method(num: int, dims=10) -> List[numpy.array]:
    dot_products = []
    for _ in range(num):
        # Create a dims x dims matrix
        x = np.random.rand(dims, dims)
        y = np.random.rand(dims, dims)
        # Create a dot product of itself
        dot_products.append(np.dot(x, y))
    return dot_products


@ray.remote
class SlowActor(object):

    def method(self, num, dims) -> None:
        return slow_method(num, dims)


if __name__ == '__main__':

    # Create an instance of SlowActor
    start = time.time()
    slow_actor = SlowActor.remote()
    results = [slow_actor.method.remote(i, 5_000) for i in range(5)]
    print(ray.get(results))
    elapsed = time.time() - start
    print(f"Time elapsed: {elapsed:.2f}")