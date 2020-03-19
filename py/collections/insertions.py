import bisect
import sys

# Sorted list of numbers were we need to insert numbers
HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
# Sorted list of numbers to add to the Haystack
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]
ROW_FMT = '{0:2d} @ {1:2d}     {2}{0:<2d}'


def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
    """
    Given breakpoint for grades, grades, and a score
    return the letter grade
    """
    i = bisect.bisect(breakpoints, score)
    return grades[i]


def demo(bisect_fn):
    # Use reverse order; more efficient
    for needle in reversed(NEEDLES):
        # Find the position
        position = bisect_fn(HAYSTACK, needle)
        offset = position * ' |'
        print(ROW_FMT.format(needle, position, offset))


if __name__ == '__main__':
    bisect_fn = bisect.bisect_left \
        if sys.argv[:-1] == 'left' else bisect.bisect
    print('DEMO:', bisect_fn.__name__)
    # use of generator expression
    print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
    demo(bisect_fn)
    print("=" * 40)
    [print(f"{grade(score)} -> {score}") for score in [33, 99, 77, 70, 89, 90, 100]]
