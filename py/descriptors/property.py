def _validate(value):
    if value <= 0:
        raise ValueError('value must be > 0')
    return value


def _validate_desc(value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value


class LineItem:

    def __init__(self, description, weight, price, number=1):
        self._description = _validate_desc(description)
        self._weight = _validate(weight)
        self._price = _validate(price)
        self._number = _validate(number)


    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = _validate_desc(value)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        self._price = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = _validate(value)

    @property
    def number(self):
        return self._number

    @weight.setter
    def number(self, value):
        self._number = _validate(value)

    def subtotal(self):
        return self._weight * self._price * self._number


def print_items(item):
    print("description: {}, weight: {}, price: {}, number: {}, subtotal: {}"
          .format(item.description, item.weight,
                  item.price, item.number, item.subtotal()))
    print(sorted(vars(item).items()))


if __name__ == '__main__':
    berries = LineItem("Brazilian berries", 20, 17.95)
    print_items(berries)
    print("--" * 5)
    # set the number
    berries.number = 10
    print_items(berries)

    # should fail
    berries.description = ""
