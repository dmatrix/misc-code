import asyncio
import time
from datetime import datetime

#
# source: https://medium.com/free-code-camp/a-guide-to-asynchronous-programming-in-python-with-asyncio-232e2afa44f6
#


async def custom_sleep(n):
    """
    Custom sleep that uses synchronous sleep

    Parameters
    ----------
    n : int
        Sleep for n seconds
    """
    print('SLEEP', datetime.now())
    time.sleep(n)


async def factorial(name, number):
    """
    A coroutine to compute a factorial

    Parameters
    ----------
    name: str
        A label to indicate which coroutine is currently running
    """

    f = 1
    for i in range(2, number + 1):
        print('Task: {}: Compute factorial for: {}'.format(name, i))
        # invoke custom sleep to yield to the next task
        await custom_sleep(2)
        f *= i
    # Print the result after having awakened after sleep
    print('Task {}: factorial({}) is {}\n'.format(name, number, f))


if __name__ == '__main__':

    # Main event loop here that queues the tasks
    start = time.time()
    loop = asyncio.get_event_loop()

    # Create a queue of tasks
    tasks = [
        asyncio.ensure_future(factorial("A", 3)),
        asyncio.ensure_future(factorial("B", 4))
    ]

    # loop until all tasks within the coroutines have been
    # scheduled and completed. These will be executed
    # synchronously because of using synchronous sleep
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    end = time.time()
    print("Total time: {}".format(end - start))

