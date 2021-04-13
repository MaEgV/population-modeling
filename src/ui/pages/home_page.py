from src.ui.pages.abstract_page import AbstractPage
import dash
import dash_core_components as dcc
import dash_html_components as html
from ..templates.dash_templates import home_page
from copy import deepcopy


class HomePage(AbstractPage):
    def __init__(self):
        self._layout = home_page()

    def get_callbacks(self):
        # Тут надо по загруженному шаблону нагенерить экземпляры классов ***_callback
        pass

    def get_layout(self):
        return deepcopy(self._layout)

