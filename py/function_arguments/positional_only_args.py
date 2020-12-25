def custom_sum(iterable, start=0):
    """
    A customer function that sum over a iterator

    Parameters
    ----------
    iterable: iterable
        An iterable object that can be specified either as keyword or positional argument

    start: int
        What number start iterating from (default is 0)

    Returns
    -------
    int
        summation of elements in the iterator
    """
    return sum(iterable) + start


def custom_sum_pos(iterable, *, start=0):
    """
    A customer function that sum over a iterator
    Takes only positional arguments before '/'


    Parameters
    ----------
    iterable: iterable
        An iterable object that can be specified *only* as a positional argument

    start: int
        What number start iterating from (default is 0)

    Returns
    -------
    int
        summation of elements in the iterator

    """
    return sum(iterable) + start


if __name__ == '__main__':
    print(custom_sum([1, 2, 3], 10))
    print(custom_sum(iterable=[1, 2, 3], start=10))
    print(custom_sum((1, 2, 3)))

    print(custom_sum_pos([1, 2, 3], start=10))
    print(custom_sum_pos(iterable=[1, 2, 3], start=10))
