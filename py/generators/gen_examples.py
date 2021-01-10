
# Some Generator function examples using yield statements

def gen_ABC():
    """
    A generator function that prints messages and blocks until the next is explicity called
    or it's used as an iterator in a for loop
    """
    print('Start')
    yield 'A'
    print('Continue ....')
    yield 'B'
    print('Continue ....')
    yield 'C'
    print('End.')


if __name__ == '__main__':

    # Use the generator function as an iterator
    # Also, generator functions allows you to create functions
    # that act as iterators

    g = gen_ABC()
    print('Using the generator function as an iterator: {}'.format(g))
    for c in g:
        print('---> {}'.format(c))

    # Use the generator function as a generator
    print('--' * 5)
    g = gen_ABC()
    print('Using the generator function as generator object: {}'.format(g))
    for _ in range(4):
        try:
            c = next(g)
            print('---> {}'.format(c))
        except StopIteration as ex:
            break
    print('--' * 5)
    # Use the generator function in a list comp
    # List comprehension is a factory of lists
    res1 = [c * 3 for c in gen_ABC()]
    for res in res1:
        print('--> {}'.format(res))
    print('--' * 5)
    # Use as a generator expression with ()
    # Generator expressions is a factory of generators
    res2 = (c * 3 for c in gen_ABC())
    print("Generator object: {}".format(res2))
    for res in res2:
        print('--> {}'.format(res))
