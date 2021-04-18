from dataclasses import dataclass, field


@dataclass
class Callback:
    args: tuple  # positional params for callback
    kwargs: dict = field(default_factory=dict)  # named parameters for callback (not required)
    func: callable = field(init=False, default=lambda x: None)  # function responsible for the return value

    def set_func(self, new_func):
        self.func = new_func

    def get_args(self):
        return self.args

    def get_kwargs(self):
        return self.kwargs

    def get_func(self):
        return self.func
