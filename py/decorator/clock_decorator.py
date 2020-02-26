import time
import functools

def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        # Invoke the function passed
        result = func(*args, **kwargs)
        elapsed_time = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(','.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k,w) for k, w in sorted(kwargs.items())]
            arg_lst.append(','.join(pairs))
        arg_str = ','.join(arg_lst)
        print('[%0.5fs] %s(%s) -> %r' % (elapsed_time, name, arg_str, result))
        return result
    return clocked

@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n-1)

if __name__ == '__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print(f"6!" is {factorial(6)})

