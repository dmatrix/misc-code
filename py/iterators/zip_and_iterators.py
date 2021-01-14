#
# source: https://medium.com/techtofreedom/7-levels-of-using-the-zip-function-in-python-a4bd22ee8bcd
#
#
from collections.abc import Iterable, Iterator
import itertools as it

if __name__ == '__main__':

    """
    Level 0: Zip aggregates items from two different iterables and
       returns an iterator
    """
    id = [1, 2, 3, 4]
    leaders = ['Elon Musk', 'Tim Cook', 'Bill Gates', 'Me']
    zip_iter = zip(id, leaders)
    print('Level: 0 ' + '--' * 5)
    print("{}: {} Is an instance of Iterator".format(isinstance(zip_iter, Iterator),
                                                     zip_iter.__class__.__name__))
    print("{}: {} Is an instance of Iterable".format(isinstance(zip_iter, Iterable),
                                                     zip_iter.__class__.__name__))

    # Construct a list from the returned zip object
    l = list(zip_iter)
    print(l)
    # create iterator again since it'll have reached its end above
    zip_iter = zip(id, leaders)
    for e in zip_iter:
        print(e)

    print('Level: 1 ' + '--' * 5)
    """
    Leve 1: Zip aggregates items from  one or more different iterables and
           returns an iterator
    """
    sex = ('male', 'male', 'male', 'NB')
    zip_iter = zip(id, leaders, sex)
    l= list(zip_iter)
    print(l)

    # Use a for loop
    zip_iter = zip(id, leaders, sex)
    for e in zip_iter:
        print(e)

    """
    Level 2: Zip aggregates items from unequal different iterables and
           returns an iterator with the shortest matching elements from both
    """
    id = [1, 2]
    zip_iter = zip(id, leaders)
    l = list(zip_iter)

    print('Level: 2 ' + '--' * 5)
    print(l)

    zip_iter = it.zip_longest(id, leaders, fillvalue='Top Gun')
    l = list(zip_iter)
    print(l)
    """
    Leve 3: Python does not have an unzip function but you can zip 
            by unpacking into respective iterables using '*' trick
    """
    record = [(1, 'Elon Musk', 'male'), (2, 'Tim Cook', 'male'), (3, 'Bill Gates', 'male'), (4, 'Me', 'NB')]
    l1, l2, l3 = zip(*record)

    print('Level: 3 ' + '--' * 5)
    print(l1, l2, l3)
    """
    Level 4: Create and Update Dictionaries by the Zip Function
    """
    id = [1, 2, 3, 4]
    leaders = ['Elon Mask', 'Tim Cook', 'Bill Gates', 'JSD']

    # create dict by dict comprehension
    # zip(..) will create a list of tuples [(id, name), (id, name)..]
    leaders_dict_1 = {i: name for i, name in zip(id, leaders)}

    # create dict by dict function
    leaders_dict_2 = dict(zip(id, leaders))

    print('Level: 4 ' + '--' * 5)
    print(leaders_dict_1)
    print(leaders_dict_2)
    assert leaders_dict_1 == leaders_dict_2

    # update the dictionary
    other_ids = [5, 6]
    other_leaders = ['Larry Page', 'Sergey Brin']
    leaders_dict_1.update(zip(other_ids, other_leaders))
    print(leaders_dict_1)
    # assert leaders_dict_1 == leaders_dict_2
    """
    Level 5: Use the Zip Function in For-Loops. You can
            use multiple iterables at the same time
    """
    products = ['apples', 'oranges', 'bananas', 'strawberries']
    prices = [2.5, 3, 5, 3.5]
    costs = [1.5, 2, 3, 2.5]

    # Use a for loop to iterate over all there iterables to calculate
    # profit, Create an interable with three tuples as a list
    print('Level: 5 ' + '--' * 5)
    for product, price, cost in zip(products, prices, costs):
        print("For product : {} the profit is ${}".format(product, price - cost))
