class MeanMaxMinMetrics(object):
    def __init__(self, name):
        self.name = name
        self.n = 0

    def __call__(self, x):
        if x < 0:
         raise ValueError("This metric cannot be negative.")
        self.n += 1
        if self.n == 1:
            self.min = x
            self.max = x
            self.mean = x
        else:
            if x < self.min:
                self.min = x
            if x > self.max:
                self.max = x
            self.mean = ((self.n - 1) * self.mean + x) / self.n

        return self

    def __str__(self):
      return f"{self.name} Metric:\n(Max: {self.max}, Min: {self.min}, Mean: {self.mean})"

if __name__ == '__main__':
   arr = list(range(10))
   metrics = MeanMaxMinMetrics("RMSE")
   for x in arr:
      print(metrics(x))
      assert metrics.mean == sum(list(range(x + 1))) / (x + 1)
      assert metrics.min == 0
      assert metrics.max == x
