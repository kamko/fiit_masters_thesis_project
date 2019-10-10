from itertools import chain
import functools


def foreach(iterable, action):
    for i in iterable:
        action(i)


def flatten_iterable(iterable):
    return chain.from_iterable(iterable)


def sleeping_iterable(min=0.1, max=2):
    from time import sleep
    from random import uniform

    def l1_wrap(func):

        def l2_wrap(*args, **kwargs):
            for i in func(*args, **kwargs):
                yield i
                sleep(uniform(min, max))
        return l2_wrap

    return l1_wrap
