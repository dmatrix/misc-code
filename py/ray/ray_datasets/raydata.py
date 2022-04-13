import ray


def compute_heavy(n):
    for _ in range(n * 2):
        f =+ (3 * n)
    return f


if __name__ == '__main__':

    ray.init()

    # Create a Dataset of Arrow records.
    records = ray.data.from_items([{"col1": i, "col2": str(i)} for i in range(10000)])
    print(records.take(5))
    print('schema:')
    print(records.schema())
    print("--" * 10)

    # Do some heavy computation with map and lambda
    ds = ray.data.range(10)
    ds2 = ds.map(lambda x: x ** x)
    print(ds.take(5), ds2.take(5))
    print(ds.count())

    ds3 = ds2.map(lambda x: compute_heavy(x))

    # ds3 is a list of object references. We need
    # to fetch them using ray.get. This call will block
    # if not ready
    print(ray.get(ds3.take(5)))
    print(ds3.count())
