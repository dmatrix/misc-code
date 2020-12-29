"""
Reduce function is an accumulative function that takes three arguments, the last one
being optional is an initializer or starting value.

Form: reduce(func(x,y), iterable, [initializer] -> Any

The function must take two elements from the iterable and apply the function to
produce a result; the result is subsequently the next new x in the iteration with
the new y picked from the iterable
"""
from functools import reduce

if __name__ == '__main__':

    num_list = [1, 2, 3, 4]
    sum_1 = reduce(lambda x, y: x + y, num_list)
    print(f'Sum of list: {num_list} is {sum_1}')
    sum_2 = reduce(lambda x, y: x + y, num_list, 2)
    print(f'Sum of list: {num_list} and initializer: {2} is {sum_2}')
    print('--' * 5)
    # product
    prod_1 = reduce(lambda x, y: x * y, num_list)
    print(f'Product of list: {num_list} is {prod_1}')
    prod_2 = reduce(lambda x, y: x * y, num_list, 2)
    print(f'Product of list: {num_list} and initializer: {2} is {prod_2}')
