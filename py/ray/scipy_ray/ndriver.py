import numpy as np
from numpy import loadtxt


def read_array(fn: str) -> np.array:
    arr = loadtxt(fn, comments="#", delimiter=',', unpack=False)
    return arr.astype('int')


def add_array(a1: np.array, a2: np.array) -> np.array:
    return np.add(a1, a2)


def sum_arr(a1: np.array) -> int:
    return a1.sum()


if __name__ == '__main__':

    arr1 = read_array("input/file_1.txt")
    print(f"array 1: {arr1}")
    arr2 = read_array("input/file_2.txt")
    print(f"array 2: {arr2}")

    result = add_array(arr1, arr2)
    print(f"Add arr1 + arr2: {result}")

    print(f'Sum of arr1: {sum_arr(arr1)}')
    print(f'Sum of arr2: {sum_arr(arr2)}')







