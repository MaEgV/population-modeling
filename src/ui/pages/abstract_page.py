from abc import abstractmethod


class AbstractPage:
    @abstractmethod
    def get_layout(self):
        raise NotImplementedError

    @abstractmethod
    def get_callbacks(self):
        raise NotImplementedError
