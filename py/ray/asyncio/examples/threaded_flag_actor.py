import random
import logging
import time
import requests
import os

import ray

FLAGS = ['CN', 'IN', 'US', 'ID', 'BR', 'PK', 'NG', 'BD', 'JP', 'MX', 'PH', 'VN', 'ET', 'EG', 'DE', 'IR', 'TR', 'CD', 'FR', 'GR']
FLAGS_URL = "http://flupy.org/data/flags"
BASE_DIR = "./downloads"


@ray.remote
class ThreadedFlagActor:

    def run_tasks(self, cc, verbose):
        if verbose:
            print(f"Started task-id='{cc}'")
        result = self.do_task(cc)
        if verbose:
            print(f"finished task=i='{cc}'")
        return result

    def do_task(self, flag):
        file_name = f"{flag.lower()}.gif"
        url = f"{FLAGS_URL}/{file_name}"
        resp = requests.get(url)
        image = resp.content
        path = os.path.join(BASE_DIR, file_name)
        with open(path, 'wb') as fp:
            fp.write(image)
        resp.close()
        time.sleep(random.randint(1, 3))

        return flag
        
if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    verbose = False
    start = time.time()
    sync_actor= ThreadedFlagActor.options(max_concurrency=len(FLAGS)).remote()
    results = ray.get([sync_actor.run_tasks.remote(cc, verbose) for cc in FLAGS])
    print(f"ThreadedFlagActor: Time elapsed:{time.time() - start:.2f}")
    print(results)