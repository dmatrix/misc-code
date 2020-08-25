from functools import wraps

def coroutine(func):
    """Decorator: primes 'func' by advancing to first yield"""
    @wraps(func)
    def primer(*args, **kwargs):
        # The decorator function is replaced with this primer function
        # Call the decorated function to get a generator object
        gen = func(*args, **kwargs)
        # Prime it
        next(gen)
        return gen
    return primer

@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    # Infinite room until .close() is sent
    while True:
        # Suspend the coroutine and produce the result to the caller
        term = yield average
        total += term
        count += 1
        average = total / count

if __name__ == "__main__":

    coro_avg = averager()
    [print(coro_avg.send(n)) for n in range(0, 50, 5)]
    coro_avg.send("Jules")
