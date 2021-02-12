"""
A factory generic function to create named tuples. Using metaprogramming,
you can create named numples on the fly, without using dataclasses
Example from Fluent Python, pg 683 (Class metaprogramming)
"""


def record_factory(cls_name, field_names):
    """
    Parameters
    ----------
        cls_name: str
            name of the class to create
    Returns
    -------
        cls_instance: class
    """
    try:
        # Split the filed names if separated by ',', otherwise
        # assume it's an iterable
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:
        # no .replace or .split, assume already a sequence of identifiers
        pass
    field_names = tuple(field_names)

    # Create attributes and methods
    def __init__(self, *args, **kwargs):
        """
        This method will become the __init__ of the created class, accepting positional
        and key-word arguments. Use slots instead of __dict__ for memory efficiency
        """
        attrs = dict(zip(self.__slots__, args))
        # include the kwargs as well
        attrs.update(kwargs)
        # now set the attributes
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):
        """
        Make this class iterable so its instances' attributes are iterable
        """
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):
        """
        Nice repr for the class instance
        """
        values = ','.join('{}={!r}'.format(*i) for i in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    # build all the class attributes, including slots and methods, as a dictionary
    cls_attrs = dict(__slots__ = field_names,
                     __init__ = __init__,
                     __iter__ = __iter__,
                     __repr__ = __repr__)

    # create an instance of this class using 'type' constructor and return
    return type(cls_name, (object, ), cls_attrs)


if __name__ == '__main__':
    # Create a class type using the factory with signature similar to named tuple
    Dog = record_factory('Dog', 'name weight owner')
    dog = Dog('Nyope', 10, 'Jules')
    print(dog)
    name, weight, _ = dog
    print("name: {}, weight {}".format(name, weight))
