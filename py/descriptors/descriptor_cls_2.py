class Quantity:
    # class attribute of Quantity keeping track of all instances created
    # this will be used to create mangle unique names for manages storage
    # attributes of the managed class
    __counter = 0

    def __init__(self):
        """
        No need for a storage name unlike the descriptor_cls.py
        """
        # reference to the Quantity class
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        # unique name for the manged stroage attribute
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
        # whatever the instance unique name formed above {_Quantity}#{index} is returned
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError("value must be > 0")


class LineItem:
    # Descriptor class instances bound to class weight, price, and number attribute
    # Note, no need to provide the label, as it will be uniquely generated
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


if __name__ == '__main__':
    coconuts = LineItem("Brazilian coconut", 20, 17.95, 5)
    print("weight: {}, price: {}, number: {}, subtotal: {}".format(coconuts.weight, coconuts.price,
                                                                   coconuts.number, coconuts.subtotal()))
    print(sorted(vars(coconuts).items()))
