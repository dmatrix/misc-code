import random
import logging
import time

import ray

@ray.remote
class SyncActor:

    def run_tasks(self, i, verbose):
        if verbose:
            print(f"Started task-id='{i}'")
        result = self.do_task(i)
        if verbose:
            print(f"finished task=i='{i}'")
        return i

    def do_task(self, i):
        time.sleep(random.randint(1, 3))
        return i
        
if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    verbose = False
    start = time.time()
    sync_actor= SyncActor.remote()
    results = ray.get([sync_actor.run_tasks.remote(i, verbose) for i in range(1, 11)])
    print(f"SyncActor: Time elapsed:{time.time() - start:.2f}")
    print(results)