"""
Another simple example from medium that illustrates the difference
between threads and processes, and also how to get around GIL
https://medium.com/towards-artificial-intelligence/the-why-when-and-how-of-using-python-multi-threading-and-multi-processing-afd1b8a8ecca
"""
import concurrent.futures as mt
import multiprocessing as mp
import time
import requests

URLs = ['http://www.python.org',
        'https://docs.python.org/3/',
        'https://docs.python.org/3/whatsnew/3.7.html',
        'https://docs.python.org/3/tutorial/index.html',
        'https://docs.python.org/3/library/index.html',
        'https://docs.python.org/3/reference/index.html',
        'https://docs.python.org/3/using/index.html',
        'https://docs.python.org/3/howto/index.html',
        'https://docs.python.org/3/installing/index.html',
        'https://docs.python.org/3/distributing/index.html',
        'https://docs.python.org/3/extending/index.html',
        'https://docs.python.org/3/c-api/index.html',
        'https://docs.python.org/3/faq/index.html'
    ]


def get_url(u):
    resp = requests.get(u)
    return resp.content


def get_cpu_count():
    return mp.cpu_count()


if __name__ == '__main__':

    # Use sequential access to fetch each urls contents
    # an I/O bound taskl
    results = []
    start = time.time()
    for url in URLs:
        content = get_url(url)
        results.append(content)
    end = time.time()
    print(f"Serial access: Time elapsed: {end - start:4.2f} for {len(results)} urls")

    # Let's try multithreading with four pool threads
    start = time.time()
    with mt.ThreadPoolExecutor(get_cpu_count()) as executor:
        results = executor.map(get_url, URLs)
    end = time.time()
    print(f"Multi Threaded access: Time elapsed: {end - start:4.2f} for {len(list(results))} urls")

    # Let's try multiprocess for each core
    # Since this is an I/O bound task, we won't get much benefit from
    # spawning processes. Threading is faster for I/O Bound tasks, and
    # multiprocessing is more efficient for CPU tasks.
    start = time.time()
    with mp.Pool(get_cpu_count()) as p:
        results = p.map(get_url, URLs)
    end = time.time()
    print(f"Multi Process access: Time elapsed: {end - start:4.2f} for {len(list(results))} urls")





