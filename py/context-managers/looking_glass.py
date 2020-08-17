import sys

#
# Example and explanation of context manager in Fluent Python

class LookingGlass:
    def __enter__(self):
        """
        Python invokes enter with no arguments besides self
        """
        # Preserve the reference to the original stdout.write
        self._original_write = sys.stdout.write
        # Monkey patch the sys.stdout.write with ours
        sys.stdout.write = self._reverse_write
        # Return some string object as part of this call to be bound
        # to a variable in the with statement is used with "as"
        return "JABBERWOCKY"

    def _reverse_write(self, text):
        """
        Function to reverse a string
        """
        # Call the monkey patched sys.stdout.write
        # which reverse the string as if looking into the mirror
        self._original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, traceback):
        """
        Python calls __exit__ with None, None, None if all went well; if an
        exception is raised, the three arguments with their respective values
        are supplied
        """
        # Restore the original sys.stdout.write
        sys.stdout.write = self._original_write
        # If exception was raised then print the message
        if exc_type is ZeroDivisionError:
            print("Please DO NOT divide by Zero. Not a good idea!")
            # Return True to tell the interpreter that exception was handled
            return True

#
# Use contextmanager decorator as an alternative to implementing a class
# Recommended in Fluent Python
#
import contextlib

@contextlib.contextmanager
def looking_glass():
    # Save the original write
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])
    # Monkey patch the stdout write
    sys.stdout.write = reverse_write
    # create msg for handling exception
    msg = ''
    try:
        yield "JABBERWOCKY"
    except ZeroDivisionError:
        msg = "Please DO NOT DIVIDE BY ZERO!"
    finally:
        # Undo monkey patch
        sys.stdout.write = original_write
        if (msg):
            print(msg)

if __name__ == '__main__':

    with LookingGlass() as what:
        print("Alice, Kitty, and Snowdrop")
        print("PySpark is great, so is MLflow!")
        print(what)

    # Should print normal
    print("Back to normal")
    print("Alice, Kitty, and Snowdrop")
    print("PySpark is great, so is MLflow!")
    print("=+" * 30)

    # Now try without the with context manager statement
    manager = LookingGlass()
    print(manager)
    monster = manager.__enter__()
    print(monster)
    manager.__exit__(None, None, None)
    print(monster)

    print("==" * 30)
    with looking_glass() as what:
        print("Alice, Kitty, and Snowdrop")
        print("PySpark is great, so is MLflow!")
        print(what)

        # Should print normal
    print("Back to normal")
    print("Alice, Kitty, and Snowdrop")
    print("PySpark is great, so is MLflow!")
