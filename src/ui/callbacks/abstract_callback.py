from abc import abstractmethod


class AbstractCallback:
    def __init__(self, params):
        self.params = params

    def get_params(self):    # [INPUT, OUTPUT, ...]
        raise NotImplementedError

    @abstractmethod
    def get_function(self):
        # CAllback implementation
        raise NotImplementedError
