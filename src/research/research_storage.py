import functools
from typing import Any, Callable

from src.research import Research


def storage(item: Any) -> Callable:
    def real_storage(func: Callable) -> Callable:
        @functools.wraps(func)
        def inner(*args: tuple, **kwargs: dict) -> Any:
            nonlocal item
            return func(item, *args, **kwargs)

        return inner

    return real_storage


@storage(Research())
def research_storage(research: Research, func: Callable) -> Callable:
    @functools.wraps(func)
    def inner(*args: tuple, **kwargs: dict) -> Any:
        return func(research, *args, **kwargs)

    return inner
