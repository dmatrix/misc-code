import numpy as np
from numpy import loadtxt


def read_array(fn: str) -> np.array:
    arr = loadtxt(fn, comments="#", delimiter=",", unpack=False)
    return arr


def add_array(a1: np.array, a2:np.array) -> np.array:
    return np.add(a1, a2)


if __name__ == '__main__':

    arr1 = read_array("input/file_1.txt")
    print(f"array 1: {arr1}")
    arr2 = read_array("input/file_2.txt")
    print(f"array 2: {arr2}")

    result = add_array(arr1, arr2)
    print(f"Add arr1 + arr2: {result}")






