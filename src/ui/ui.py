import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from pandas import DataFrame
import numpy as np
from dash.dependencies import Output, Input, State
from .pages.abstract_page import AbstractPage


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

storage = dict()

class DashUI:
    def __init__(self, callbacks: dict):
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

        self.app.title = "Avocado Analytics: Understand Your Avocados!"
        self.app.layout = html.Div()
        global storage
        storage = callbacks
        self.app.layout = html.Div(
                                children=[
                                    html.Div(dcc.Input(id='input-box', type='text')),
                                    html.Button('Submit', id='button'),
                                    html.Div(id='output-container-button',
                                             children='Enter a value and press submit'),
                                    html.Div(
                                        children=dcc.Graph(
                                            id="price-chart", config={"displayModeBar": False},
                                        ),
                                        className="card",
                                    )
                                ],
                                className="wrapper",
                            )

    def run(self):
        self.app.run_server(debug=True, host='127.0.0.1')

    def add_callback(self, function, in_list):
        @self.app.callback(*in_list)
        def inner(*args, **kwargs):
            function(*args, **kwargs)