import logging
import sqlite3
import time
import random

import ray
from utils import NPI_DB, SQL_QUERIES

@ray.remote
class SyncSQLiteActor:

    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile, check_same_thread=False)
        
    def run_tasks(self, q, verbose=True):
        if verbose:
            print(f"Started task-id='{q}'")
        s = time.time()
        result = self.do_query(q)
        n = time.time() - s
        if verbose:
            print(f"finished task-id='{q} in {n:2f} secs'")
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
    start = time.time()
    sync_actor = SyncSQLiteActor.remote(NPI_DB)
    results = ray.get([sync_actor.run_tasks.remote(query, verbose) for query in SQL_QUERIES])
    print(f"SyncActor: Time elapsed:{time.time() - start:.2f}; for {len(SQL_QUERIES)} SQLite queries")
    print(results)