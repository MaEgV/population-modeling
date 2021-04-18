import dash_core_components as dcc
import dash_html_components as html
from typing import List

from src.population.mutations.normal_mutator import NormalMutator
from src.ui.callback import Callback
from dash.dependencies import Output, Input, State
from dataclasses import dataclass, field
import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [4, 1, 4],
    'c': ['x', 'y', 'z'],
})


class HomeTemplate:
    _children: list = [
        html.Div([
            html.Label('Selector'),
            dcc.Dropdown(
                options=[
                    {'label': 'Default Selector', 'value': 'Default Selector'}
                ],
                value='Default Selector',
                id='selector'),
            html.Label('Mutator'),
            dcc.Dropdown(
                options=[
                    {'label': 'Normal Mutator', 'value': 'NormalMutator()'}
                ],
                value='NormalMutator()',
                id='mutator'),
        ],
            style={'width': '40%'},
        ),
        html.Button('Build', id='build', n_clicks=0),
        html.Div([html.Label('Maximum bacteria lifetime'),
                  dcc.Slider(
                      min=0,
                      max=15,
                      step=1,
                      marks={
                          0: '0',
                          1: '1',
                          2: '2',
                          3: '3',
                          4: '4',
                          5: '5',
                          6: '6',
                          7: '7',
                          8: '8',
                          9: '9',
                          10: '10',
                          11: '11',
                          12: '12',
                          13: '13',
                          14: '14',
                          15: '15'
                      },
                      value=5,
                      id='lifetime'
                  ),
                  html.Label('Death probability'),
                  dcc.Slider(
                      min=0,
                      max=1,
                      step=0.1,
                      marks={
                          0: '0',
                          1: '1'
                      },
                      value=0.5,
                      id='death'
                  ),
                  html.Label('Reproduction probability'),
                  dcc.Slider(
                      min=0,
                      max=1,
                      step=0.1,
                      marks={
                          0: '0',
                          1: '1'
                      },
                      value=0.5,
                      id='reproduction'

                  ),
                  ],
                 style={'width': '40%', 'position': 'relative', 'left': '50%'},
                 ),
        html.Button('Add', id='add', n_clicks=0, style={'position': 'relative', 'left': '43%'}),
        html.Div(id='output', style={'width': '40%', 'position': 'relative', 'left': '50%'}),
        html.Div(id='graph')]

    _callbacks: list = [Callback((Output('output', 'children'),
                                 State('reproduction', 'value'),
                                 State('death', 'value')),
                                 {'prevent_initial_call': True}),
                        Callback((Output('graph', 'children'),
                                  Input('add', 'n_clicks'),
                                  State('lifetime', 'value'),
                                  State('death', 'value'),
                                  State('reproduction', 'value')),
                                 {'prevent_initial_call': True}),
                        Callback((Output('reproduction', 'min'),), {'prevent_initial_call': True})
                        ]

    @staticmethod
    def get_children():
        return HomeTemplate._children

    @staticmethod
    def get_callbacks():
        return HomeTemplate._callbacks
