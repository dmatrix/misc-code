import sys
import time


def decorator_func_logger(target_func):
    """
    Our decorator function that extends the target_func's functionality.
    Decorator pattern allows you as a developer to extend your existing utility of functions
    or classes. That is, in a case where you want to use all these existing functions but need
    some additional custom logic, you can decorate an existing function, implement your custom
    logic without having the need repeat the code
    
    Usage1 : No arguments and no multiple decorators
    Parameters
    ----------
    target_func: function
        The target function object that needs decoration and extention

    Returns
    -------
        wrapper: function
            Returns a wrapper function
    """
    def wrapper_func():
        print(f'Before calling the target function: {target_func.__name__}')
        target_func()
        print(f'After calling the target function: {target_func.__name__}')

    return wrapper_func


@decorator_func_logger
def target():
    """
    Our target function that is decorated
    """
    print(f'Inside the decorated target function: {sys._getframe().f_code.co_name} being decorated')


def decorator_func_logger_2(target_func):
    """
    Usage 2: Multiple decorators and arguments to decorators functions
    Parameters
    ----------
    target_func: function
        The target function object that needs decoration and extention

    Returns
    -------
        wrapper: function
            Returns a wrapper function
    """
    def wrapper_func(*args, **kwargs):
        """
        Parameters
        ----------
        args: tuple
            Packed unplaced tuple of positional arguments
        kwargs: dict
            Keyword arguments
        Returns
        -------
        wrapper: function
            Returns a wrapper function
        """
        print(f'Before calling the target function: {target_func.__name__}')
        target_func(*args, **kwargs)
        print(f'After calling the target function: {target_func.__name__}')

    return wrapper_func


def decorator_func_timeit(target_func):
    """
    Decorators times the target_func. That is, it extends its functionality
    """
    def wrapper_func(*args, **kwargs):
        ts = time.time()
        target_func(*args, **kwargs)
        te = time.time()
        print(f'Time elapsed in {target_func.__name__}: {(te-ts) * 1000}')

    return wrapper_func


@decorator_func_logger_2
@decorator_func_timeit
def target_loop(*args, **kwargs):
    """
    Function decorated with multiple decorators.
    """
    count = 0
    print(f'Inside the decorated target function w/ arguments: {sys._getframe().f_code.co_name} being decorated')
    for num in range(*args):
        count += num
    if kwargs:
        print(f'kwargs: {kwargs}')


if __name__ == '__main__':
    target()
    print("--" * 10)
    target_loop(100, 200, times=2, name='Jules')
