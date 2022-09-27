import logging
import sqlite3
import time
import random

import ray
from utils import NPI_DB, SQL_QUERIES

@ray.remote
class ThreadedSQLiteActor:

    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile, check_same_thread=False)

    def run_tasks(self, q, verbose=True):
        if verbose:
            print(f"Started task-id='{q}'")
        result = self.do_query(q)
        if verbose:
            print(f"finished task=i='{q}'")
        return result

    def do_query(self, q):
        result = self.conn.execute(q).fetchall()
        time.sleep(random.randint(1,3))
        return len(result)
        
if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    verbose = False
    max_concurrency = len(SQL_QUERIES)
    start = time.time()
    threaded_actor = ThreadedSQLiteActor.options(max_concurrency=max_concurrency).remote(NPI_DB)
    results = ray.get([threaded_actor.run_tasks.remote(query, verbose) for query in SQL_QUERIES])
    print(f"ThreadedActor: Time elapsed:{time.time() - start:.2f}; concurrency level: {max_concurrency} for {max_concurrency} SQLite queries")
    print(results)