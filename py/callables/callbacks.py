import sys


class MyClass(object):
    """
    Class demonstrating how to register and invoke callbacks
    """
    def __init__(self):
        super(MyClass, self).__init__()
        self.pre_hooks = []
        self.post_hooks = []
        self.n_hooks = 0

    def __call__(self, *args, **kwargs):
        if self.pre_hooks:
            self._hooks(self.pre_hooks, *args, **kwargs)
            self.n_hooks += len(self.pre_hooks)

        if self.post_hooks:
            self._hooks(self.post_hooks, *args, **kwargs)
            self.n_hooks += len(self.post_hooks)

        return self.n_hooks

    def add_callbacks(self, pre_callbacks=None, post_callbacks=None):
        if pre_callbacks:
            self.pre_hooks = [h for h in pre_callbacks]
        if post_callbacks:
            self.post_hooks = [h for h in post_callbacks]

        return self

    def _hooks(self, callbacks, *args, **kwargs):
        for callback in callbacks:
            callback(*args, **kwargs)


def pre_hook_callback(*args, **kwargs):
    print('Inside function: {}'.format(sys._getframe().f_code.co_name))
    a = [arg for arg in args]
    print('args: {}'. format(a))
    kw = [(k, v) for k, v in kwargs.items()]
    print('kwargs: {}'.format(kw))


def post_hook_callback(*args, **kwargs):
    print('Inside function: {}'.format(sys._getframe().f_code.co_name))
    a = [arg for arg in args]
    print('args: {}'.format(a))
    kw = [(k, v) for k, v in kwargs.items()]
    print('kwargs: {}'.format(kw))


if __name__ == '__main__':
    c = MyClass()
    c.add_callbacks(pre_callbacks=[pre_hook_callback])\
        .add_callbacks(post_callbacks=[post_hook_callback])
    res = c("lr", "lgm", "xgboost", 'svm', l_rate=5, n_iter=5, n_fold=2, lr2=0.05)
    print('Total hooks executed: {}'.format(res))
    print('--' * 5)
    res = c("xgboost", 'svm', l_rate=5, n_iter=5, n_fold=2, lr2=0.05)

