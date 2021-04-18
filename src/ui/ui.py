import sys

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from pandas import DataFrame
import numpy as np
from dash.dependencies import Output, Input, State

from .callback import Callback
from .pages.abstract_page import AbstractPage

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]


class DashUI:
    def __init__(self, page: AbstractPage):
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        self.app.layout = page.get_layout()
        self.add_callbacks(page.get_callbacks())

    def add_callbacks(self, callbacks: list):
        for callback in callbacks:
            add_callback(self.app, callback)

    def run(self):
        self.app.run_server(debug=True, host='127.0.0.1')


def add_callback(app, callback: Callback):
    @app.callback(callback.get_args(), **callback.get_kwargs())
    def inner(*args, **kwargs):
        return callback.get_func()(*args, **kwargs)
