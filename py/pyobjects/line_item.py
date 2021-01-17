"""
Validating a Property item, dynamically accessing or adding a new Property or attribute
"""


class LineItem(object):
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # the property is checked if negative or < 0
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def __getattr__(self, item):
        # check if it has an item
        if hasattr(self.__dict__, item):
            return getattr(self.__dict__(), item)
        return None

    def __setattr__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            super().__setattr__(key, value)

    @classmethod
    def new_instance(cls, *args):
        return cls(*args)

    @property
    def weight(self):
        return self.__weight   # the actual value is stored in the private attribute __weight

    @weight.setter
    def weight(self, value):
        if value > 0:          # only set value > 0 in the private attribute __
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    def __repr__(self):
        class_name = type(self).__name__
        return '({!r}, {!r}, {!r}, {!r})'.format(class_name, self.description, self.weight, self.price)

    def __eq__(self, other):
        return (self.description == other.description and
                self.price == other.price and
                self.weight == other.weight)


if __name__ == '__main__':
    line_item = LineItem('Fluent Python', 14, 56.00)
    print(line_item)
    print("subtotal: {}".format(line_item.subtotal()))
    line_item_2 = LineItem.new_instance('Fluent Python', 14, 56.00)
    print("subtotal: {}".format(line_item_2.subtotal()))
    print(id(line_item), id(line_item_2))
    if line_item.author is None:
        setattr(line_item, 'author', 'Luciano Ramalho')
    print(line_item.author)
    assert line_item == line_item_2
    print(line_item.__dict__.items())
