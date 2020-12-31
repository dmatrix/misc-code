def func_args(f_name, l_name=None, initial=None):
    """
    Positional and keyword arguments format

    Parameters
    ----------
    f_name : str
        First name
    l_name : str, optional
        last name (default is None)
    initial: str, optional
        inital letter (default is None)

    Returns
    -------
    str
        a concanated string of type full name
    """
    full_name = f_name + ' ' + initial + ' ' + l_name if initial else f_name + ' ' + l_name
    return full_name


if __name__ == '__main__':

    print(func_args("Jules", l_name='Damji', initial='S.'))
    print(func_args('Jules', 'Damji', 'S.'))
    print(func_args('Jules', 'Damji'))

    # For named-keyword, the order does not matter when supplied with named=value
    print(func_args("Jules", initial='S.', l_name='Damji'))

    # Must supply the first  positional argument
    print(func_args(l_name='Damji', initial='F.'))
