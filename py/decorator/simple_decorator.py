import warnings

registry = []

"""
Define a decorator function
"""
def deco(func):
    def inner():
        print('running inner()')
    return inner

""""
Decorated Function using the decorator
"""
@deco
def target():
    print("running target")

"""
Decorator to register a function
"""
def register(func):
    print(f"Running register {func}")
    registry.append(func)
    return func

"""
Decorated function using the decorator register
"""
@register
def f1():
    print("Running f1")


@register
def f2():
    print("Running f2")


def f3():
    print("Running f3")


def main():
    print("Running main()")
    print(f"Registry -> {registry}")
    f1()
    f2()
    f3()


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    target()
    print(f"target is {target}")
    main()


