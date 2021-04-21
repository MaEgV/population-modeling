import functools
from src.research import Research


def storage(item):
    def real_storage(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            nonlocal item
            return func(item, *args, **kwargs)

        return inner

    return real_storage


@storage(Research())
def research_storage(research, func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(research, *args, **kwargs)

    return inner
