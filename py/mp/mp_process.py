import multiprocessing as mp
import os


def f(x):
    pid = os.getpid()
    ppid = os.getppid()
    res = x ** 2
    print(f"Parent pid: {ppid}, Child pid: {pid}, res :{res}")


if __name__ == '__main__':
    cores = mp.cpu_count()
    print(f"number of cores: {cores}")
    processes = []
    mp.set_start_method('fork', force=True)
    for core in range(cores):
        process = mp.Process(target=f, args=[core+1])
        processes.append(process)
        process.start()
    for proc in processes:
        proc.join()
