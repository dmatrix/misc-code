import multiprocessing as mp
import os


def f(x):
    pid = os.getpid()
    ppid = os.getppid()
    res = x ** 2
    print(f"Parent pid: {ppid}, Child pid: {pid}, res :{res}")
    return res


if __name__ == '__main__':
    cores = mp.cpu_count()
    print(f"number of cores: {cores}")
    with mp.Pool() as p:
        results = p.map(f, range(20))
        print(results)
