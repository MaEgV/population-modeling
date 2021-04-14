import dash_core_components as dcc
import dash_html_components as html
from src.ui.callback import Callback
from dash.dependencies import Output, Input, State
from dataclasses import dataclass, field


class HomeTemplate:
    _children: list = [
        html.Button(id='button'),
        dcc.Graph(id='main_graph'),
        html.Div(id='global-data', style={'display': 'none'}),  # Global storage on client side
    ]

    _callbacks: list = [
        # Graph
        Callback(
            (Output('main_graph', 'figure'),
             Input('button', 'n_clicks')),
            lambda: None
        ),

        # # Graph redrawer
        # Callback(
        #     (Output('main_graph', 'figure'),
        #      Input('global-data', 'children')),
        #     lambda: None
        # )
    ]

    @staticmethod
    def get_children():
        return HomeTemplate._children

    @staticmethod
    def get_callbacks():
        return HomeTemplate._callbacks
