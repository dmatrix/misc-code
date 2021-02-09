def op_decorator(func):
    """
    Decorator to decorate a function
    Parameters
    ----------
        func: func to be decorated

    Returns
    --------
        wrapper function
    """
    def wrapper_func(*args):
        print("-- {} operation is called with parameter(s) {}".format(func.__name__, args))

        # Invoke the decorated function
        return func(*args)
    return wrapper_func


@op_decorator
def add(x, y):
    return x + y


@op_decorator
def sub(x, y):
    return x - y


@op_decorator
def mul(x, y):
    return x * y


@op_decorator
def div(x, y):
    return x / y


if __name__ == '__main__':
    print(add(4, 2))
    print(sub(4, 2))
    print(mul(4, 2))
    print(div(4, 2))




