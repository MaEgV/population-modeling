from dataclasses import dataclass, field
from typing import Callable, Any


@dataclass
class Callback:
    """
    A class that stores the inputs and outputs for a callback and its implementation
    """
    args: tuple  # positional params for callback
    kwargs: dict = field(default_factory=dict)  # named parameters for callback (not required)
    _func: Callable = field(init=False, default=lambda x: None)  # function responsible for the return value

    def set_func(self, new_func: Callable) -> None:
        self._func = new_func# type: ignore

    def get_args(self) -> tuple:
        return self.args

    def get_kwargs(self) -> dict:
        return self.kwargs

    def get_func(self) -> Callable:
        return self._func
