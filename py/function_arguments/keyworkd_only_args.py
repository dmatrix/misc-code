def func_args(a='a', b='b', c='c', d=None):
    """
    Keyword only arguments
    Two things to note:
    Args can be supplied in order of signature without named keyword
    Args can be supplied with out-of-order but with named keyword and value

    Positional and keyword argument format

    Parameters
    ----------
    a: str
        optional, default is 'a'
    b: str, optional
        optional, default is 'b'
    c: str, optional
        optional, default is 'c'
    d: str, optional
        optional, default is 'd'

    Returns
    -------
    list
        a list of arguments in the signature order
    """
    return [a, b, c, d]

def func_args_1(*, a, b):
    """
    Keyword only arguments
    Two things to note:
    Args can be supplied in order of signature without named keyword
    Args can be supplied with out-of-order but with named keyword and value

    Positional and keyword argument format

    Parameters
    ----------
    a: str
        first argument
    b: str, optional
        second argument

    Returns
    -------
    list
        a list of arguments in the signature order
    """
    return [a, b]


def func_args_2(a, *, mult1=1, mult_2=2):
    """
    This signature with * enforces to take  only one positional argument
    before the '*'

    Parameters
    ----------

    a: int
        number to add to arguments
    mult1: int
        number to multiply with (default is 1)
    mult2: int
        number to multiply with (default is 2)

    Returns
    -------
    int
        the result of the expression

    """
    return (a + mult1) * mult_2


if __name__ == '__main__':
    print(func_args('Jules', 'Damji', 'S', 'J'))
    print(func_args(d='J', a='Jules', b='Damji', c='S'))
    print(func_args(a='Jules', b='Damji', c='S'))

    # this enforces keyword argument only
    print(func_args_1(a="Jules", b='Damji'))
    print(func_args_1(b="Damji", a="Jules"))

    # this enforces to only one positoinal argument
    print(func_args_2(4, mult_2=5, mult1=3))

    # generates an error if more than one positional argusment
    print(func_args_2(4, 5))
