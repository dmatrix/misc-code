import logging
import aiosqlite
import time
import asyncio
import random

import ray
from utils import NPI_DB, SQL_QUERIES

@ray.remote
class AsyncSQLIteActor:
    
    async def __init__(self, dbfile):
        self.db_file = dbfile
        self.conn = await self._create_conn()

    async def _create_conn(self):
        return await aiosqlite.connect( self.db_file, check_same_thread=False)

    async def run_tasks(self, q, verbose=True):
        if verbose:
            print(f"Started task-id='{q}'")
        result = await self.do_query(q)
        if verbose:
            print(f"finished task=i='{q}'")
        return result

    async def do_query(self, q):
        cursor = await self.conn.execute(q)
        result = await cursor.fetchall()
        await cursor.close()
        await asyncio.sleep(random.randint(1,3))
        return len(result)

if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    verbose = False
    start = time.time()
    max_concurrency = len(SQL_QUERIES)
    async_actor = AsyncSQLIteActor.options(max_concurrency=max_concurrency).remote(NPI_DB)
    results = ray.get([async_actor.run_tasks.remote(query, verbose) for query in SQL_QUERIES])
    end = time.time() - start
    print(f"AsyncActor: Time elapsed:{time.time() - start:.2f}; concurrency level: {max_concurrency} for {max_concurrency} SQLite queries")
    print(results)
