#
# This simple class is one of the several Callable flavors in Python
# By implementing its __call__ method, this object is callable.
# Example borrowed, and modified, from "Fluent Python" by Luciano Ramalho.
# (A must book to have if you want to be fluent in Python!
#
import random

class BingoCage():
    '''
    Constructor takes an iterable
    :param an iterable list
    '''

    def __init__(self, items):
        self._items = list(items)
        # shuffle the items randomly
        random.shuffle(self.items)

    @property
    def items(self):
        return self._items

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from an empty BingoCage')

    def __call__(self):
        return self.pick()

class Averager():
    """"
    Python class that keeps a running metrics of min, max, and mean.
    """
    def __init__(self, stock_sym):
        self._stock_sym = stock_sym
        self.count = 0
        self.total = 0
        self.max_value = 0
        self.min_value = 0

    @property
    def stock_sym(self):
        return self._stock_sym

    def __call__(self, new_value):
        '''
        callable class instance. Computes running mean, max, and min
        values
        '''
        self.count += 1
        self.total += new_value
        if new_value <= self.min_value:
            self.min_value = new_value
        if new_value >= self.max_value:
            self.max_value = new_value
        return (self.total / self.count, self.max_value, self.min_value)


if __name__ == "__main__":
    fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana', 'avacado']
    bingo = BingoCage(fruits)
    print(bingo())
    print(bingo.pick())
    [print(bingo()) for n in range(3)]
    print(bingo.items)
    print(dir(bingo))
    print ("=" * 80)
    avg = Averager("DBX")
    print(f"Stats for Stock Symbol {avg.stock_sym}")
    [print(avg(num)) for num in range(10, 25, 2)]
    print(avg(10))
    print(avg(12))

