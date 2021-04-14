import dash_core_components as dcc
import dash_html_components as html
from src.ui.callback import Callback
from dash.dependencies import Output, Input, State
from dataclasses import dataclass, field


class HomeTemplate:
    _children: list = [
            html.Button(id='button'),
            dcc.Graph(id='price-chart')
        ]

    _callbacks: list = [
                Callback(
                    (Output('price-chart', 'children'),
                     [Input('button', 'n_clicks')]),
                    lambda: None
                )
        ]

    @staticmethod
    def get_children():
        return HomeTemplate._children

    @staticmethod
    def get_callbacks():
        return HomeTemplate._callbacks
