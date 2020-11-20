
# Define a class Duck with two behaviors (methods)
# that you can expect from ducks
class Duck:

    def swim(self):
       print("I can swim")

    def quack(self):
        print("I can quack")


def duck_testing(obj):
    try:
        obj.swim()
        obj.quack()
    except AttributeError:
        print("I'm not a duck")
    else:
        print("I'm a duck!")


class ToyDuck:

    def swim(self):
       print("I can swim")

    def quack(self):
        print("I can quack")

class Human:

    def swim(self):
       print("I can swim")


if __name__ == '__main__':
    duck = Duck()

    # this is an instance of Duck class
    print(isinstance(duck, Duck))
    duck_testing(duck)

    toy_duck = ToyDuck()

    # this is not an instance of Duck class
    # but passes the behavior of the duck class
    # The idea of duck typing is not so much about an
    # object being an instance but about behaving like
    # an instance. Here toy_duck behaves like a Duck

    # It’s just the supported behaviors (i.e., swim and quack)
    # that make the toy_duck a duck-like object and pass the duck
    # typing test. It’s the key to implementing duck typing.
    print(isinstance(toy_duck, Duck))
    duck_testing(toy_duck)

    # Now let's take an example of Human
    human = Human()
    print(isinstance(human, Duck))
    duck_testing(human)
