"""
Filter is another function, like map, it iterates over elements of an iterable
and filters or keeps only elements who condition is True for the expression or
function supplied

Form; filter(func, iterable) -> filterObject
"""

if __name__ == '__main__':

    list_num = [i for i in range(25)]
    odd_list = list(filter(lambda x: x % 2 == 1, list_num))
    even_list = list(filter(lambda x: x % 2 == 0, list_num))
    print(f'odd list: {odd_list}')
    print(f'even_list: {even_list}')

    # Using list comps and lambda
    odd_squared_list_1 = [x ** 2 for x in range(25) if x % 1 == 0]
    print(f'odd list: {odd_squared_list_1}')
    odd_squared_list_2 = list(map(lambda x: x**2, filter(lambda x: x % 1 == 0, range(25))))
    print(f'odd list: {odd_squared_list_2}')
    assert odd_squared_list_1 == odd_squared_list_2

