import itertools
import operator
"""
Use of iterators using itertools
https://towardsdatascience.com/7-python-iterators-you-maybe-didnt-know-about-a8f4c9aea981
"""


def sqr(n):
    return n ** 2


def sum_of_sqrs(x, y):
    return sqr(x) + sqr(y)


def is_prime(n):
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


if __name__ == '__main__':

    # 1. itertools.count(). Start counting at 10
    for i in map(sqr, itertools.count(10)):
        # exit when the i**2 value returned from the map exceeds 1000
        if i > 1000:
            break
        print(i)

    # 2. itertools.cycle(). Iterate until exhausts the iterable
    # creates a list of tuplles with zip[(A, 0), (B, 1), (C, 3) ...)
    a = "ABCDEFGHI"
    print(list(zip(a, itertools.cycle(range(3)))))

    # 3. itertools.chain(). Chain iterables together
    list_1 = "ABCD"
    list_2 = "EFGH"
    set_1 = ('a', 'b')
    set_2 = ('c', 'd')
    tuple_1 = ((1, 2), (3, 4))
    tuple_2 = ((5, 6), (7, 8))
    print(list(itertools.chain(list_1, list_2, list_1)))
    print(list(itertools.chain(set_1, set_2)))
    print(list(itertools.chain(tuple_1, tuple_2)))

    # 4. itertools.starmap()... takes a function that takes multiple parameters
    # Use list comp to create tuples (x, x+1)
    res_tuples = [(x, x+1) for x in range(5)]
    print(res_tuples)
    print(list(itertools.starmap(sum_of_sqrs, res_tuples)))

    # 5. Create a cartesian product from an iterable
    a = [1, 2, 3, 4]
    print(list(itertools.product(a, repeat=2)))

    # 6. Generate a particular slice from an iterable
    # For example, itertools.isplice(gen, start, stop),
    # to return a list starting a start, and stopping at stop

    gen = itertools.count()   # create an infinite generator
    print(list(itertools.islice(gen, 2, 10)))  # start at 2, and stop at 10

    # 7. itertools.accumulate()  # is like fold, and can take operator type
    op = operator.mul        # use the add operator

    list_1 = [1, 2, 3, 4]
    print(list(itertools.accumulate(list_1)))
    print(list(itertools.accumulate(list_1, func=op)))




