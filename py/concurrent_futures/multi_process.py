import multiprocessing as mp
import os


def f(name):
    print('hello {} from pid: {}'.format(name, os.getpid()))
    print('Inherited env MLFLOW_TRACKING_TOKEN: {}', os.environ.get('MLFLOW_TRACKING_TOKEN'))


if __name__ == '__main__':
    processes = []
    os.environ['MLFLOW_TRACKING_TOKEN'] = 'foobar'
    mp.set_start_method('fork')
    for _ in range(4):
        p = mp.Process(target=f, args=['Jules'])
        processes.append(p)
        p.start()

    for proc in processes:
        proc.join()
