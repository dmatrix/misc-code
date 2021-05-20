import random
import os
import time
import multiprocessing

import ray


def local_task():
    return sum(x * x for x in range(random.randint(1, 25)))


@ray.remote
def remote_task(a, b):
    print("pid={}; ppid={}".format(os.getpid(), os.getppid()))
    return sum(x * x for x in range(random.randint(a, b)))


if __name__ == '__main__':

    n_cores = multiprocessing.cpu_count()
    print("Number of cores: {}".format(n_cores))
    # Initialize on the local host
    ray.init(num_cpus=n_cores)

    # invoke local task
    print("Local return valued: {}". format(local_task()))

    # invoke remote ray task
    for _ in range(n_cores):
        print("Remote Ray task returned value: {}".format(ray.get(remote_task.remote(1000, 1000000))))

    time.sleep(10000)



