class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value

if __name__ == "__main__":
    # Creating instances
    singleton1 = Singleton('First')
    singleton2 = Singleton('Second')

    print(singleton1.value)  # Output: First
    print(singleton2.value)  # Output: First
    print(singleton1 is singleton2)  # Output: True
    print(singleton1 == singleton2)  # Output: True
    print(singleton1.__dict__)  # Output: {'value': 'First'}
    print(singleton2.__dict__)  # Output: {'value': 'First'}
