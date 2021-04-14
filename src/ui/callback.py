from dataclasses import dataclass


@dataclass
class Callback:
    params: tuple
    func: callable

    def set_func(self, new_func):
        self.func = new_func

    def get_params(self):
        return self.params

    def get_function(self):
        return self.func
