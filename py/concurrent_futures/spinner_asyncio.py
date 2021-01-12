import asyncio
import itertools
import sys


async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            # Yield from to suspend the coroutine without blocking
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            # wakes up the coroutine and exits the loop
            break
    write(' ' * len(status) + '\x08' * len(status))


async def slow_function():
    """
    this now a coroutine and uses yield from to let the event
    loop proceed while this coroutine pretends to do I/O by sleeping
    """
    await asyncio.sleep(3)
    return 42


async def supervisor():
    """
    It's a coroutine too, so it can drive slow_function with yield from
    """
    #
    # create an async task object that wraps spin function
    spinner = asyncio.create_task(spin('thinking'))
    print(spinner)
    result = await slow_function()
    spinner.cancel()
    return result


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer: {}'.format(result))


if __name__ == '__main__':
    main()
