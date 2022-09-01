import os
import time
import multiprocessing
import math
import ray

START_POINTS = [1, 100, 1000, 10000]
END_POINTS = [1000, 10000, 100000, 1000000]


def none_ray_task(a: int, b: int) -> int:
    return math.sqrt(sum(x * x for x in range(a, b)))


def print_pairs(a: int, b: int) -> None:
    print((a, b))


@ray.remote(num_cpus=3)
def ray_task(a: int, b: int) -> int:
    print("pid={}; ppid={}".format(os.getpid(), os.getppid()))
    return math.sqrt(sum(x * x for x in range(a, b)))


if __name__ == '__main__':

    n_cores = multiprocessing.cpu_count()
    print("Number of cores: {}".format(n_cores))

    # invoke local task
    start = time.time()
    for _ in range(n_cores):
        print("Local return valued: {:.2f}". format(none_ray_task(1, 10000)))
    print("Time elapsed for non ray task: {:.2f}".format(time.time() - start))

    # Initialize on the local host
    ray.init(num_cpus=n_cores)
    start = time.time()
    for _ in range(n_cores):
        print("Remote Ray task returned value: {:.2f}".format(ray.get(ray_task.remote(1, 10000))))
    print("Time elapsed for non Ray task: {:.2f}".format(time.time() - start))

    [print_pairs(s, e) for s in START_POINTS for e in END_POINTS]
    time.sleep(10)



