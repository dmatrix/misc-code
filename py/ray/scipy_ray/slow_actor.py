import time

import numpy as np
import ray


@ray.remote
class SlowActor(object):

    def method(self) -> None:
        for _ in range(10):
            # Create a 1000 x 1000 matrix of 1s
            x = np.ones((1000, 1000))
            # Create a dot product of itself
            np.dot(x, x)


def slow_method(actor: object, num: int) -> None:
    for _ in range(num):
        actor.method.remote()


if __name__ == '__main__':

    # Create an instance of SlowActor
    slow_actor = SlowActor.remote()
    print(f"Object Reference for SlowActor: {slow_actor})")
    slow_method(slow_actor, 50)
    # time.sleep(1000)