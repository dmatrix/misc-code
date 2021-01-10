def averager():
    """
    Coroutine that yields until closed. This function keeps
    track of a running average of some metric, say term
    """
    total = 0.0
    count = 0
    average = None

    # Infinite room until .close() is sent
    while True:
        # Suspend the coroutine and produce the result to the caller
        # when send is invoked
        term = yield average
        total += term
        count += 1
        average = total/count


if __name__ == "__main__":

    # Create a coroutine object
    coro_avg = averager()

    # Priming or initializing the coroutine
    next(coro_avg)
    print(coro_avg.send(10))
    print(coro_avg.send(5))
    print(coro_avg.send(5))

    # Terminate the coroutine
    coro_avg.close()

