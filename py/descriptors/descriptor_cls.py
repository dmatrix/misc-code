"""
Some definitions for Descriptor concepts

Descriptor Class
----------------
    A class implementing the descriptor protocol. That is, it has its __get__, __set__, or
    __delete__ methods

Managed Class
-------------
    The class where the descriptor instances are declared as class attributes.

Descriptor Instance
-------------------
    Each instance of a descriptor, declared as class attribute of the managed class.

Managed Instance
----------------
    A single instance of the managed class above.

Storage Attribute
-----------------
    A crucial concept to understand, this is an attribute of the managed instance that will
    hold the value of managed attribute for that particular instance. Often, it will have the
    same variable name as the instance attributes. See example below.

Managed Attribute
-----------------
    A public attribute in the managed class that will be handled by a descriptor instance, with
    values stores in the storage attributes. In other words, a descriptor instance and a storage
    attribute provide the infrastructure for a managed attribute

    Pg 651: Fluent Python
"""


class Quantity:
    """
    A descriptor class implementing a descriptor protocol with __get__ and __set__methods
    """
    def __init__(self, storage_name):
        """
        Parameters
        ----------
        storage_name: str
            Name of where data for each property is stored.
        """
        # Each Quantity instance will have a unique storage_name attribute.
        # This is the name of the attribute that will hold the value of managed instances
        self.storage_name = storage_name

    def __set__(self, instance, value):
        """
        This is called when a value is assigned to the managed attribute. For example
        LineItem.weight or LineItem.price

        Parameters
        ----------
            self: descriptor instance
            instance: managed instance
        """
        if value > 0:
            # We must assign to the managed instance dict directly; trying to use
            # setattr built-in would trigger the __set__ method again, leading to
            # infinite recursion
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError("value must be > 0")


class LineItem:

    # Descriptor class instances bound to class weight and price attribute
    weight = Quantity('weight')
    price = Quantity('price')
    number = Quantity('number')

    def __init__(self, description, weight, price, number=1):
        self.description = description

        # managed Attributes
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
    print("weight: {}, price: {}, number: {}, subtotal: {}".format(nutmeg.weight, nutmeg.price,
                                                                   nutmeg.number, nutmeg.subtotal()))
    print(sorted(vars(nutmeg).items()))
    print(LineItem.price, LineItem.weight, LineItem.number)

    # Add newer managed instance attributes
    nutmeg.foobar = 'foo'
    print(sorted(vars(nutmeg).items()))
    nutmeg.foobar = 'jules'
    print(sorted(vars(nutmeg).items()))
    print(nutmeg.foobar)
    print(sorted(LineItem.__dict__.items()))
