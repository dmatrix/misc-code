import ray

CVS_FILE_PATH = "data/windfarm_data.csv"


@ray.remote
def cube(n):
    return n * n * n


if __name__ == '__main__':

    data = ray.data.read_csv(CVS_FILE_PATH)
    print(data.take(3))
    print("schema:")
    print(data.schema())

    ds = ray.data.range(10000)
    ds2 = ds.map(lambda x: x ** x)
    ds3 = ds2.map(lambda x: cube.remote(x))

    print(ds.take(5), ds2.take(5), ray.get(ds3.take(5)))
    print(ds.count())

    # Create a Dataset of Arrow records.
    records = ray.data.from_items([{"col1": i, "col2": str(i)} for i in range(10000)])
    print(records.take(5))
    print('schema:')
    print(records.schema())
