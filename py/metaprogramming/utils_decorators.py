"""
Wrapper utility functions that will act as decorators to methods we add to the class
dynamically.
"""


def debug_function(func):
    def wrapper(*args, **kwargs):
        print(" -- operation: {} is called with parameter:s {}".format(func.__qualname__, args[1:]))
        return func(*args, **kwargs)
    return wrapper


def debug_all_methods(cls):
    for key, val in vars(cls).items():
        if callable(val):
            # Dynamically decorate this method
            setattr(cls, key, debug_function(val))

    # Return the modified methods
    return cls
