import multiprocessing as mp
import os


def f(conn):
    """
    Function runs in the process and gets queue to add something to it
    """
    items = [42, None, 'Jules']
    pid = os.getpid()
    p_pid = os.getppid()
    conn.send(items)
    conn.close()
    print(f"Parent pid: {p_pid}, Child pid: {pid}, items sent to the Pipe :{items}")


if __name__ == '__main__':
    parent_conn, child_conn = mp.Pipe()
    p = mp.Process(target=f, args=(child_conn,))
    p.start()
    print(f"Items fetched from the Parent end of the pipe: {parent_conn.recv()}")
    p.join()
