import string

"""
Derived from: https://towardsdatascience.com/three-functions-to-know-in-python-4f2d27a4d05
Map function allows to take function and apply it against each element
in an iterator and add to the map object. The list function then casts
all elements of the map object and retuns a list that is assigned to squared_list

Form: map(func, Iterable)
"""

abc = string.ascii_lowercase


def encrypt(m, n):
    """
    Encrypt a message

    Parameters
    ----------
    m: str
        Ascii lowercase string to encrypt
    n: int
        Number of spaces

    Returns
    -------
    str
        Ascii encrypted string
    """
    return ''.join(map(lambda x: abc[(abc.index(x)+n) % 26] if x in abc else x, m))


def decrypt(code, n):
    """
    Encrypt a message

    Parameters
    ----------
    code: str
        Ascii lowercase string to encrypt
    n: int
        Number of spaces

    Returns
    -------
    str
        Ascii encrypted string
    """
    return ''.join(map(lambda x:abc[(abc.index(x)-n) % 26] if x in abc else x, coded))


if __name__ == '__main__':
    num_list = [1, 2, 3, 4]
    squared_list = list(map(lambda x: x ** 2, num_list))
    print(f'type: {type(squared_list)}, contents:{squared_list}')

    # another interesting example of coding and decoding a string
    msg = "My password is: jules/&*pass!"
    coded = encrypt(msg, 2)
    decoded = decrypt(coded, 2)
    print("encoded: {}".format(coded))
    print("decoded: {}".format(decoded))
