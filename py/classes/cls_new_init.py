"""
The example is to show how to use __new__ and __init__ to create a new instance.
"""
class MyClass:
    def __new__(cls, *args, **kwargs):
        print("__new__ method is called")
        instance = super().__new__(cls)
        return instance

    def __init__(self, value_1, value_2, **kwargs):
        print("__init__ method is called")
        self.instance_variable_1 = value_1
        self.instance_variable_2 = value_2
        self._dict = kwargs

        for key, value in kwargs.items():
            setattr(self, key, value)

if __name__ == "__main__":
    obj = MyClass(5, 6, name="John", age=25, city="New York")
    print(obj.instance_variable_1, obj.instance_variable_2)  # 5 6
    print(obj._dict)  # {'name': 'John', 'age': 25, 'city': 'New York'}
    print(obj.__dict__)  # {}  # The instance variable is not in the instance's __dict__.
    print(MyClass.__dict__)  # {'__module__': '__main__', '__new__': <function MyClass.__new__ at