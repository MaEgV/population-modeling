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

        add_callbacks(self.app, page.get_callbacks())

    def run(self):
        self.app.run_server(debug=True, host='127.0.0.1')


def add_callbacks(app, callbacks: list):
    for callback in callbacks:
        @app.callback(*(callback.get_params()))
        def inner(*args, **kwargs):
            return callback.get_function()(*args, **kwargs)
