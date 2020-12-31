def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)
    return averager


class Averager():
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append((new_value))
        total = sum(self.series)

        return total/len(self.series)


if __name__ == "__main__":
    avg = Averager()
    [print(avg(num)) for num in range(10, 20)]
    print(avg(10))
    print(avg(12))
    print(avg.series)
    print("-" * 10)
    avg = make_averager()
    [print(avg(num)) for num in range(10, 20)]
    print(avg(10))
    print(avg(12))

