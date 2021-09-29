import numpy as np
from numpy import loadtxt
import ray

#
# Ray converts decorated functions into stateless tasks, scheduled
# anywhere onto a ray worker in the cluster
#


@ray.remote
def read_array(fn: str) -> np.array:
    arr = loadtxt(fn, comments="#", delimiter=",", unpack=False)
    return arr.astype('int')


@ray.remote
def add_array(a1: np.array, a2: np.array) -> np.array:
    return np.add(a1, a2)


@ray.remote
def sum_arr(a1: np.array) -> int:
    return a1.sum()


if __name__ == '__main__':

    # Ray executes immediately and returns a future
    # Futures in Ray enable parallelism
    obj_ref_arr1 = read_array.remote("input/file_1.txt")
    print(f"array 1: {obj_ref_arr1}")
    obj_ref_arr2 = read_array.remote("input/file_2.txt")
    print(f"array 2: {obj_ref_arr2}")

    # Ray executes immediately and returns a future
    result_obj_ref = add_array.remote(obj_ref_arr1, obj_ref_arr2)

    # Fetch the result: this will block if not finished
    result = ray.get(result_obj_ref)
    print(f"Result: add arr1 + arr2: {result}")

    # Add the array elements and get the sum
    sum_1 = ray.get(sum_arr.remote(obj_ref_arr1))
    sum_2 = ray.get(sum_arr.remote(obj_ref_arr2))

    print(f'Sum of arr1: {sum_1}')
    print(f'Sum of arr2: {sum_2}')






