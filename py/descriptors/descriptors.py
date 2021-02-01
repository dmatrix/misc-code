"""
A general and refactored classes for implementation of Descriptor classes
for storage and validation

Fluent Python: pg 662
"""

import abc


class AutoStorage:
    """
    AutoStorage provides the most of the functionality of the former Quantity descriptor
    in descriptor_cls_2.py
    """
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        """
        This is called when the managed instance's managed attribute is accessed
        Uses the built-in getattr to the get value from the instance

        Parameters
        ----------
            self: class instance
            instance: managed instance
            owner: reference to the managed class (e.g., LineItem)

        Returns
        -------
            value of the managed attribute
        """
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        # validation will be handled by the Validated class
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):

    def __set__(self, instance, value):
        # call the abstract method of the parent class that will do
        # the validation and return the value
        value = self.validate(instance, value)
        # call AutoStorage.__set__()
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """return the validate value or raise ValueError"""


class Quantity(Validated):
    """ Validate a number greater than zero"""
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """ validate a string with at least a single character"""
    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value


class LineItem:
    description = NonBlank()
    weight = Quantity()
    price = Quantity()
    number = Quantity()

    def __init__(self, description, weight, price, number=1):
        self.description = description
        self.weight = weight
        self.price = price
        self.number = number

    def subtotal(self):
        return self.weight * self.price * self.number
