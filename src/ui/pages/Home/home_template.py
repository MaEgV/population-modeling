import dash_core_components as dcc
import dash_html_components as html
from src.ui.callback import Callback
from dash.dependencies import Output, Input, State
import plotly.express as px


class HomeTemplate:
    _children: list = [
        html.Div([
            html.Label('Selector'),
            dcc.Dropdown(id='selector'),
            dcc.Slider(id='selector_value'),
            html.Label('Mutator'),
            dcc.Dropdown(id='mutator'),
            dcc.Slider(id='mutator_value'),
            html.Label('Iterations: '),
            dcc.Input(id='iterations', type='number', placeholder='number of iterations')
        ],
            style={'width': '40%'},
        ),
        html.Button('Build', id='build', n_clicks=0),
        html.Button('Rebuild', id='rebuild', n_clicks=0),
        html.Div([html.Label('Maximum bacteria lifetime'),
                  dcc.Slider(id='lifetime'),
                  html.Label('Death probability'),
                  dcc.Slider(id='death'),
                  html.Label('Reproduction probability'),
                  dcc.Slider(id='reproduction'),
                  html.Div(id='void'),
                  ],
                 style={'width': '40%', 'position': 'relative', 'left': '50%'},
                 ),
        html.Button('Add', id='add', n_clicks=0, style={'position': 'relative', 'left': '43%'}),
        html.Div(id='output', style={'width': '40%', 'position': 'relative', 'left': '50%'},
                 children='Choose parameters'),
        html.Div([dcc.Graph(id='graph', figure=px.scatter())]),
        html.Div(id='hidden')]

    _callbacks: list = [Callback((Output('output', 'children'),
                                  Input('death', 'value'),
                                  Input('reproduction', 'value')
                                  ),
                                 {'prevent_initial_call': True}),
                        Callback((Output('void', 'children'),
                                  Input('add', 'n_clicks'),
                                  State('lifetime', 'value'),
                                  State('death', 'value'),
                                  State('reproduction', 'value')),
                                 {'prevent_initial_call': True}),
                        Callback((Output('graph', 'figure'),
                                  Input('build', 'n_clicks'),
                                  State('iterations', 'value'),
                                  State('selector', 'value'),
                                  State('selector_value', 'value'),
                                  State('mutator', 'value'),
                                  State('mutator_value', 'value')),
                                 {'prevent_initial_call': True}),
                        Callback((Output('selector', 'options'),
                                  Output('selector', 'value'),
                                  Output('selector_value', 'min'),
                                  Output('selector_value', 'max'),
                                  Output('selector_value', 'step'),
                                  Output('selector_value', 'value'),
                                  Output('selector_value', 'marks'),
                                  Input('hidden', 'id'))),
                        Callback((Output('mutator', 'options'),
                                  Output('mutator', 'value'),
                                  Output('mutator_value', 'min'),
                                  Output('mutator_value', 'max'),
                                  Output('mutator_value', 'step'),
                                  Output('mutator_value', 'value'),
                                  Output('mutator_value', 'marks'),
                                  Input('hidden', 'id'))),
                        Callback((Output('lifetime', 'min'),
                                  Output('lifetime', 'max'),
                                  Output('lifetime', 'step'),
                                  Output('lifetime', 'marks'),
                                  Output('lifetime', 'value'),
                                  Output('death', 'min'),
                                  Output('death', 'max'),
                                  Output('death', 'step'),
                                  Output('death', 'marks'),
                                  Output('death', 'value'),
                                  Output('reproduction', 'min'),
                                  Output('reproduction', 'max'),
                                  Output('reproduction', 'step'),
                                  Output('reproduction', 'marks'),
                                  Output('reproduction', 'value'),
                                  Input('hidden', 'id')
                                  ))
                        ]

    @staticmethod
    def get_children():
        return HomeTemplate._children

    @staticmethod
    def get_callbacks():
        return HomeTemplate._callbacks
