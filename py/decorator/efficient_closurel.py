# Python closure
def make_averager():
    count = 0
    total = 0
    min_value = 0
    max_value = 0

    def averager(new_value):
        nonlocal count, total, min_value, max_value
        count += 1
        total += new_value
        if new_value <= min_value:
            min_value = new_value
        if new_value >= max_value:
            max_value = new_value
        return (total / count, max_value, min_value)

    return averager

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

if __name__ == '__main__':

    # Using Python class
    avg = Averager("DBX")
    print(f"Stats for Stock Symbol {avg.stock_sym}")
    [print(avg(num)) for num in range(10, 25, 2)]
    print(avg(10))
    print(avg(12))
    print("-" * 10)
    # Using Python closure
    avg = make_averager()
    [print(avg(num)) for num in range(10, 25, 2)]
    print(avg(10))
    print(avg(12))

