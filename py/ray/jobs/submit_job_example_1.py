import time

import numpy as np
import ray
from ray.util.multiprocessing import Pool


def task(n):
    time.sleep(0.005 * n)
    
    array_1 = np.random.randint(n*50, size=n) * 0.05
    array_2 = np.random.randint(n * 50, size=n) * 0.03

    return np.sum(array_1) + np.sum(array_2)


@ray.remote
def launch_long_running_tasks(num_pool=5):
    # doing the work, collecting data, updating the database
    # create an Actor pool of num_pool workers nodes
    pool = Pool(num_pool)
    results = []
    for result in pool.map(task, range(1, 500, 10)):
        results.append(result)
    pool.terminate()
    return results


@ray.remote
class LaunchDistributedTasks:
    def __init__(self, limit=10):
        self._limit = limit

    def launch(self):
        # launch the remote task
        return launch_long_running_tasks.remote(self._limit)


if __name__ == '__main__':
    ray.init()
    hdl = LaunchDistributedTasks.remote()
    print("Launched remote jobs")
    values = ray.get(ray.get(hdl.launch.remote()))
    print(f" list of results :{values}")
    print(f" Total results: {len(values)}")

