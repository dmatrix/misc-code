from collections import namedtuple

Result = namedtuple('Result', 'count average')


# Define the subgenerator
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        # Each value sent by the client code in the main() will be bound to term here
        term = yield
        # The crucial terminating condition value sent by client in the main(). Without
        # it, a yield from calling this coroutine will block forever
        if term is None:
            break
        total += term
        count += 1
        average = total / count
        # The returned Result will be the value of the yield from expression in grouper
        return Result(count, average)


# The delegating generator
def grouper(results, key):
    # Each iteration in this loop creates a new instance of averager; each
    # is a generator because it yields a value
    while True:
        # Whenever grouper is sent a value, it's piped into the averager
        # instance by the yield from. grouper will be suspended here as long
        # the averager is consuming values sent by the client. When an averager
        # instance runs to the end, the value it returns is bound to results[key].
        # The while then proceeds to create another instance of averager to consume
        # subsequent values.
        results[key] = yield from averager()


# The client code a.ka. the caller
def main(data):
    results = {}
    for key, values in data.items():
        # group is a generator object resulting from calling grouper
        # with the results dictionary to collect the results and a
        # particular key. It operates as a coroutine to which you
        # can send values

        group = grouper(results, key)

        # prime the coroutine
        next(group)

        # send each value into the grouper. That value ends up in the term = yield
        # line of the averager; grouper never has a chance to see it.
        for value in values:
            group.send(value)

        # sending None into the grouper causes the current averager instance to terminate
        # and allows grouper to run again, which creates another averager for the next
        # group of values.
        group.send(None)


    print(results)
    report(results)


# Output report
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:2f}{}'.format(
            result.count, group, result.average, unit))

data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46]
}
if __name__ == '__main__':
    main(data)
