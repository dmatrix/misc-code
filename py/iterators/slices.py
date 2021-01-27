"""
Simple illustration of slice notation on interators
source: https://medium.com/better-programming/how-to-get-the-last-item-in-a-list-in-python-2608078ddc70

slice(start, [stop], [step]) is a constructor in python that returns an object. It returns slice of a
given object; slice notation [start, stop, step] iterates over
an iterator, starting at 'start', stopping at 'stop', and stepping by 'step'

Below are few examples of slice notations
"""

if __name__ == "__main__":
    name = "Jules Damji"
    numbers = [100, 200, 300, 400]

    # get a slice object, starting at 1, stopping at 3
    s = slice(0, 3)
    print(name[s])
    print(numbers[s])
    print("--" * 5)

    # start at index 1, step forward one at a time
    print(name[1:])
    print(numbers[1:])
    print("--" * 5)

    # start at index 0, step forward one at a time and stop at index 2
    print(numbers[0:2])
    print(name[0:2])
    print("--" * 5)

    # step backwards every two items
    print(name[::-2])
    print(numbers[::-2])
    print("--" * 5)

    # step backwards one at a time, reverse it
    print(numbers[s])
    print(numbers[::-1])
    print(name[::-1])




