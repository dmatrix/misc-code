import string

if __name__ == '__main__':

    """
    Usage 1: Build dictionary from a list of keys
    """
    keys = list(string.ascii_lowercase)
    params = dict.fromkeys(keys)
    print(params)

    # Using list comp
    items = [c for c in string.ascii_lowercase]
    params = dict.fromkeys(items)
    print(params)

    print('--' * 5)
    """
    Usage 2: Convert between lists and dictionaries
    """
    #  A list of tuples
    items = [("a", 1), ("b", 2), ("c", 3)]
    params = dict(items)
    print(params)

    #  A list of list if tuples
    items = [["a", 1], ["b", 2], ("c", 3)]
    params = dict(items)
    print(params)

    # A zip object
    items = zip(["a", "b", "c"], [1, 2, 3])
    params = dict(items)
    print(params)
    keys = [i for i in range(1, 26)]
    values = list(string.ascii_lowercase)
    items = zip(keys, values)
    params = dict(items)
    print(params)

    """
    Usage 3: create lists from dictionaries
    """

    print('--' * 5)
    existing_dict_1 = {"a": 1, "b": 2, "c": 3}
    existing_dict_2 = params
    list_1 = list(existing_dict_1)
    list_2 = list(existing_dict_1.keys())
    print(f'list_1: {list_1}')
    print(f'list_2: {list_2}')
    assert list_1 == list_2
    list_3 = list(existing_dict_1.items())
    print(f'list_3 as list of k,v: {list_3}')

    """
    Usage 4: Dictionary comprehensions
    """
    print('--' * 5)

    # Create square dictionary
    existing_list = [1, 2, 3]
    square_dict = [{x: x**2} for x in existing_list]
    print(square_dict)

    # create odd number dictionary
    odd_dict = [{x: x**2} for x in existing_list if x % 2 == 1]
    print(odd_dict)

    """
    Using pop() popitem() dictionary methods
    """
    grades = {"John": 'C', "Jane": 'A', "Zico": 'F'}
    grade = grades.pop('John')
    print(f"name: {'John'}; grade: {grade}; grades: {grades}")
    name, grade = grades.popitem()
    print(f"name: {name}; grade: {grade}; grades: {grades}")
    print(grades.pop('jon', 'NA'))
