import logging
import sqlite3
import time

import ray
from utils import NPI_DB, SQL_QUERIES

@ray.remote
class SyncActor:

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
        return len(result)
        
if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)
    verbose = False
    start = time.time()
    sync_actor = SyncActor.remote(NPI_DB)
    results = ray.get([sync_actor.run_tasks.remote(query, verbose) for query in SQL_QUERIES])
    print(f"SyncActor: Time elapsed:{time.time() - start:.2f}")
    if verbose:
        print(results)