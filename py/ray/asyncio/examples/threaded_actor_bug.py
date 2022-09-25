import ray

import logging
import time

import ray

SQL_QUERIES = ["SELECT * FROM npi_data WHERE lower(city)='houston'",
               "SELECT * FROM npi_data WHERE lower(city)='athens'",
               "SELECT * FROM npi_data WHERE lower(city)='athens' and state='TX'",
               "SELECT * FROM npi_data WHERE city LIKE 'A___'",
               "SELECT * FROM npi_data WHERE city LIKE 'B___'",
               "SELECT * FROM npi_data WHERE city LIKE 'C___'",
               "SELECT * FROM npi_data WHERE city LIKE 'D___'",
               "SELECT * FROM npi_data WHERE city LIKE 'E___'",
               "SELECT * FROM npi_data WHERE city LIKE 'F___'",
               "SELECT * FROM npi_data WHERE city LIKE 'G___'",
               "SELECT * FROM npi_data WHERE city LIKE 'H___'",
               "SELECT * FROM npi_data WHERE city LIKE 'I___'",
               "SELECT * FROM npi_data WHERE city LIKE 'J___'",
               "SELECT * FROM npi_data WHERE city LIKE 'K___'",
               "SELECT * FROM npi_data WHERE city LIKE 'L___'",
               "SELECT * FROM npi_data WHERE city LIKE 'M___'",
               "SELECT * FROM npi_data WHERE city LIKE 'N___'",
               "SELECT * FROM npi_data WHERE city LIKE 'O___'",
               "SELECT * FROM npi_data WHERE city LIKE 'P___'",
               "SELECT * FROM npi_data WHERE city LIKE 'Q___'",
               "SELECT * FROM npi_data WHERE city LIKE 'R___'",
               "SELECT * FROM npi_data WHERE city LIKE 'S___'",
               "SELECT * FROM npi_data WHERE city LIKE 'T___'",
               "SELECT * FROM npi_data WHERE city LIKE 'U___'",
               "SELECT * FROM npi_data WHERE city LIKE 'V___'",
               "SELECT * FROM npi_data WHERE city LIKE 'W___'",
               "SELECT * FROM npi_data WHERE city LIKE 'X___'",
               "SELECT * FROM npi_data WHERE city LIKE 'Y___'",
               "SELECT * FROM npi_data WHERE city LIKE 'Z___'",
               "SELECT * FROM npi_data WHERE city LIKE 'Z___' and state='IL'",
               "SELECT * FROM npi_data WHERE city LIKE 'Z___' and state='IL' and name like 'MA%'",
               "SELECT * FROM npi_data GROUP BY city, state",
               "SELECT * FROM npi_data"
]

@ray.remote
class ThreadedActorBug:

    def __init__(self, dbfile):
        self.dbfile = dbfile

    def run_tasks(self, q, verbose=True):
        if verbose:
            print(f"Started task-id='{q}'")
        result = self.do_query(q)
        if verbose:
            print(f"finished task=i='{q}'")
        return result

    def do_query(self, q):
        time.sleep(2)
        return len(q)
        
if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    verbose = False
    for c in range(2, 26, 2):
        start = time.time()
        threaded_actor_bug = ThreadedActorBug.options(max_concurrency=c).remote("foo")
        results = ray.get([threaded_actor_bug.run_tasks.remote(query, verbose) for query in SQL_QUERIES])
        print(f"ThreadedActorBug: Time elapsed:{time.time() - start:.2f}; concurrency level: {c}")
    print(results)