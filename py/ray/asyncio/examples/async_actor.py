import random
import logging
import time
import asyncio
import random

import ray

@ray.remote
class AsyncActor:

   async def run_tasks(self, i, verbose):
        if verbose:
            print(f"Started task-id='{i}'")
        result = await self.do_task(i)
        if verbose:
            print(f"finished task=i='{i}'")
        return i

   async def do_task(self, i):
        await asyncio.sleep(random.randint(1, 3))
        return i
        
if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    verbose = False
    start = time.time()
    async_actor= AsyncActor.options(max_concurrency=10).remote()
    results = ray.get([async_actor.run_tasks.remote(i, verbose) for i in range(1, 11)])
    print(f"AsyncActor: Time elapsed:{time.time() - start:.2f}")
    print(results)