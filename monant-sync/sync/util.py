from itertools import chain


def foreach(iterable, action):
    for i in iterable:
        action(i)


def flatten_iterable(iterable):
    return chain.from_iterable(iterable)
