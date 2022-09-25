import logging
import asyncio
import sqlite3
import time

import ray
from utils import NPI_DB, SQL_QUERIES

@ray.remote
class AsyncActor:
    
    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile, check_same_thread=False)

    async def run_tasks(self, q, verbose=True):
        if verbose:
            print(f"Started task-id='{q}'")
        result = await asyncio.gather(self.do_query(q))
        if verbose:
            print(f"finished task=i='{q}'")
        return result

    async def do_query(self, q):
        result = self.conn.execute(q).fetchall()
        return len(result)

if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)
    verbose = False
    for c in range(2, 28, 2):
        start = time.time()
        async_actor = AsyncActor.options(max_concurrency=c).remote(NPI_DB)
        results = ray.get([async_actor.run_tasks.remote(query, verbose) for query in SQL_QUERIES])
        end = time.time() - start
        print(f"AsyncActor: Time elapsed:{time.time() - start:.2f}; concurrency level: {c}")
    print(results)
