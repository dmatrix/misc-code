"""
A monkey patch is a way for a program to extend or modify supporting
system software locally (affecting only the running instance of
the program). — Wikipedia

As a dynamic language, Python allows us to use monkey patching in
our coding by extending specific modules or classes without modifying
their original implementations. That is one can replace or inject
dynamically new code in place of the original code.
"""
from duck_typing import Duck, Human, duck_testing

class Foo:
    attr1 = "Atrribute_1"

    def bar(self):
        pass

def bar2(f):
    print("bar 2 func of Foo")

def quack(presumed_duck):
    print("I can quack")

if __name__ == '__main__':

    # Since class Foo in Python is an object, like everything else
    # you can dynammically access all its attributes
    print(dict(Foo.__dict__))

    # Monkey patching allows us to add or replace existing atrtributes
    Foo.attr2 = "Atrribute_2"
    Foo.bar2 = bar2
    print(dict(Foo.__dict__))
    f = Foo()
    print(f.bar2())

    # Let's monkey patch Human to be a duck
    Human.quack = quack
    donald_duck = Human()

    print(dict(Human.__dict__))

    duck_testing(donald_duck)

