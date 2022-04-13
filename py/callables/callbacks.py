import sys
import time


class MyClass(object):
    """
    Class demonstrating how to register and invoke callbacks
    """
    def __init__(self, pre_callbacks=None, post_callbacks=None):
        super(MyClass, self).__init__()
        self.pre_hooks = []
        self.post_hooks = []

        # Register callbacks if any
        if pre_callbacks:
            self.pre_hooks = [h for h in pre_callbacks]
        if post_callbacks:
            self.post_hooks = [h for h in post_callbacks]
        self.n_hooks = 0

    def __call__(self, *args, **kwargs):
        # Execute your pre-hooks here
        if self.pre_hooks:
            self._execute_hooks(self.pre_hooks, *args, **kwargs)
            self.n_hooks += len(self.pre_hooks)
        #
        # your callable logic here
        #
        self._do_work(self, *args, **kwargs)

        # Execute your post hooks
        if self.post_hooks:
            self._execute_hooks(self.post_hooks, *args, **kwargs)
            self.n_hooks += len(self.post_hooks)

        return self.n_hooks

    def _execute_hooks(self, callbacks, *args, **kwargs):
        for callback in callbacks:
            callback(*args, **kwargs)

    def _do_work(self, *args, **kwargs):
        print('Inside function: {}'.format(sys._getframe().f_code.co_name))
        print("Executing ... search")
        time.sleep(1.5)
        print("Building ... indexes")
        time.sleep(1.5)
        print("Saving ... indexes")
        time.sleep(1.5)
        print("Done")
        print('--' * 5)


def pre_hook_callback(*args, **kwargs):
    print('Inside function: {}'.format(sys._getframe().f_code.co_name))
    a = [arg for arg in args]
    print('args: {}'. format(a))
    kw = [(k, v) for k, v in kwargs.items()]
    print('kwargs: {}'.format(kw))
    print("Checking ... indexes")
    time.sleep(1.5)
    print("Done")


def hook_cleanup(*args, **kwargs):
    print(f"Inside function: {sys._getframe().f_code.co_name}")
    print("cleaning up ... indexes")
    time.sleep(1.5)
    print("All cached and saved indexes cleaned up!")


def post_hook_callback(*args, **kwargs):
    print('Inside function: {}'.format(sys._getframe().f_code.co_name))
    a = [arg for arg in args]
    print('args: {}'.format(a))
    kw = [(k, v) for k, v in kwargs.items()]
    print('kwargs: {}'.format(kw))
    print("verifying ... indexes")
    time.sleep(1.5)
    print("Done")


if __name__ == '__main__':
    cls = MyClass(pre_callbacks=[pre_hook_callback], \
                  post_callbacks=[post_hook_callback, hook_cleanup])

    res = cls("lr", "lgm", "xgboost", 'svm', l_rate=5, n_iter=5, n_fold=2, lr2=0.05)
    print('Total hooks executed: {}'.format(res))
    print('--' * 5)
    res = cls('ray-xgboost', 'tune', l_rate=5, n_iter=5, n_fold=2, lr2=0.05)
    print('Total hooks executed: {}'.format(res))

