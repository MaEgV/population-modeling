import dash_html_components as html
from ..abstract_page import AbstractPage
from copy import deepcopy
from .home_template import HomeTemplate


def _init_id():
    last_id = 0

    def get_id():
        nonlocal last_id
        last_id += 1
        return last_id - 1

    return f'home_temp_{get_id()}'


class HomePage(AbstractPage):
    template = HomeTemplate()

    @staticmethod
    def _init_callbacks(functions):
        callbacks = deepcopy(HomePage.template.get_callbacks())

        for key in callbacks.keys():
            callbacks[key].set_func(functions[key])

        return callbacks

    def __init__(self, functions):
        self._callbacks = HomePage._init_callbacks(functions)
        self.id = _init_id()

    def get_layout(self):
        return html.Div(
                id=self.id,
                children=HomePage.template.get_children()
           )

    def get_callbacks(self):
        return self._callbacks.values()
