from ray.util.multiprocessing import Pool

def f(index):
    return index

pool = Pool()
print(type(pool))
for result in pool.map(f, range(10)):
    print(result)