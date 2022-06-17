import time

from ray.util.multiprocessing import Pool


def f(index):
    time.sleep(5)
    return index


if __name__ == "__main__":
    pool = Pool(5)
    for result in pool.map(f, range(10)):
        print(result)