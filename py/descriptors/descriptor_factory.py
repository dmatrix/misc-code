"""
How to use property as factory for getters and setters
"""


def quantity(storage_name: str) -> property:
    """
    Higher order function as a factory, with closures that use getters and setter
    as closures. The property class is returned

    Parameters
    ----------
        storage_name: str
            Name of where data for each property is stored.

    Returns
    -------
        property
    """

    def qty_getter(instance):
        return instance.__dict__[storage_name]

    def qty_setter(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItem:
    weight = quantity('weight') # use the factory to create a class attribute for quantity
    price = quantity('price')   # use the factory to create a class attribute for price
    number = quantity('number') # use the factory to create a class attribute for number

    def __init__(self, description, weight, price, number=1):
        self.description = description
        self.weight = weight
        self.price = price
        self.number = number

    def subtotal(self):
        return self.weight * self.price * self.number


if __name__ == '__main__':
    nutmeg = LineItem('Moluccan netmeg', 8, 13.95, 10)
    print("weight: {}, price: {}, subtotal: {}".format(nutmeg.weight, nutmeg.price, nutmeg.subtotal()))
    print(sorted(vars(nutmeg).items()))
    nutmeg.number = 1
    print("weight: {}, price: {}, subtotal: {}".format(nutmeg.weight, nutmeg.price, nutmeg.subtotal()))
    print(sorted(vars(nutmeg).items()))
    print(LineItem.price, LineItem.weight)
