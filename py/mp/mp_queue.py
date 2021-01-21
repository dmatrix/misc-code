import multiprocessing as mp
import os


def f(q):
    """
    Function runs in the process and gets queue to add something to it
    """
    items = [42, None, 'Jules']
    q.put(items)
    pid = os.getpid()
    p_pid = os.getppid()
    print(f"Parent pid: {p_pid}, Child pid: {pid}, items added to Queue :{items}")


if __name__ == '__main__':
    q = mp.Queue()
    p = mp.Process(target=f, args=(q,))
    p.start()
    print(f"Items fetched from the Queue: {q.get()}")
    p.join()
