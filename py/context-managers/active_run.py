class ActiveRun:
    """Wrapper around :py:class:`mlflow.entities.Run` to enable using Python ``with`` syntax."""

    def __enter__(self):
        return 'STARTED'

    def __exit__(self, exc_type, exc_val, exc_tb):
        status = "FINISHED" if exc_type is None else "FAILED"
        return exc_type is None

#
# Use contextmanager decorator as an alternative to implementing a class
# Recommended in Fluent Python
#
import contextlib

@contextlib.contextmanager
def active_run():
    msg = ""
    try:
        yield 'STARTED'
    except Exception as ex:
        msg = "Exception Occurred"
        return True
    finally:
        if (msg):
            print(msg)


if __name__ == '__main__':

    # run as a class
    with ActiveRun() as what:
        print(what)
    print("=+" * 4)
    # run as a function
    with active_run() as run:
        print(run)

