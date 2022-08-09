import ray
import time
import random
import numpy as np


@ray.remote(num_cpus=1)
class Actor:
    def __init__(self):
        self.a = np.arange(10).reshape(2, 5)

    def f(self):
        time.sleep(random.randint(1, 5))
        self.a *= random.randint(5, 15)
        return self.a.sum()


if __name__ == "__main__":
    ray.init()
    actors = [Actor.remote() for _ in range(10)]
    refs = [a.f.remote() for a in actors]
    results = ray.get(refs)
    print(results)
