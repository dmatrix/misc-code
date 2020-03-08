#
# Think of registry, as the name sugguests, a global factory where
# functions are registered or deregistered
#
# Make this a set of additions and deletions are efficient
registry = set()

def register(active=True):
    '''
    Take an optional keyword argument to register the function,
    default is True
    '''
    def decorate(func):
        '''
        The acutal decorator that takes func as an argument
        '''
        print(f"Running register(active={active}) -> decorate({func}")
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        # Because decorate is a decorator it must return a func
        return func
    # Register our decorator factory so it returns decorate
    return decorate

@register(active=False)
def f1():
    print("Running f1()")

@register()
def f2():
    print("Running f2()")

@register()
def f3():
    print("Running f2()")

def main():
    print("-" * 70)
    print(registry)
    print("running main:")
    f1()
    f2()
    f3()

if __name__ == "__main__":
    main()
