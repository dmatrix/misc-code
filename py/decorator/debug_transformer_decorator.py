"""
Define the decorator function as a transformer
source: https://medium.com/swlh/demystifying-python-decorators-in-10-minutes-ffe092723c6c
Modified to return values and take arguments
"""
import time


def debug_transfomer(func):
    def wrapper(*args, **kwargs):
        print(f"Function `{func.__name__} called`")
        # And pass it to the original function
        res = func(*args, **kwargs)
        print(f"Function `{func.__name__} finished`")
        return res

    # return function object
    return wrapper


@debug_transfomer
def walkout(msg):
    """
    Decorated function with the decorator
    """
    print(f'{msg}')
    return (msg, len(msg))


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f'Time elapsed: {elapsed}')

        return elapsed
    return wrapper


@time_it
def waste_time(n):
    for _ in range(n):
        pass


if __name__ == '__main__':
    for name in ["Julio", "Cesar", "Dos", "Santos"]:
        r = walkout(name)
        print(r)

    waste_time(10000000)
