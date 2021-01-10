# Example from Fluent Python to show how to implement s spinner
# using a single thread. Then we'll show how to achieve the same
# result using python's asyncio without threads
import threading
import itertools
import time
import sys


class Signal:
    """
    Class with a simple mutable object go to control the main thread
    """
    go = True


def spin(msg, signal):
    """"
    This function runs in a separate thread than main.

    Parameters
    ----------
    msg: str
        msg to print on the console

    signal: class Signal
    """
    write, flush = sys.stdout.write, sys.stdout.flush

    # Infinite loop until thread is stopped
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        # Trick to do text-mode animation
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:
            break
    # Trick to clear the status line
    write(' ' * len(status) + '\x08' * len(status))


def slow_function():
    """
    Imitate some costly function

    Returns
    -------
    int
        return a constant 42, the answer to the universe
    """
    # Pretend waiting for some I/O
    time.sleep(4)
    return 42


def supervisor():
    """
    This function sets up secondary thread, displays the thread object, runs the
    slow computation, and kills the thread

    Returns
    -------
    int
        The value of the computed result
    """
    signal = Signal()
    spinner = threading.Thread(target=spin, args=('thinking', signal))
    print('spinner object: {}'.format(spinner))
    spinner.start()

    # Run the slow function, which will block the main thread, while the spinner
    # is animating
    result = slow_function()

    # Change the status of the Signal so we can stop the spinner thread, which
    # is running the spin function
    signal.go = False

    # wait until the spinner thread finishes
    spinner.join()
    return result


def main():
    """
    The main driver
    """
    result = supervisor()
    print(result)


if __name__ == '__main__':
    main()
