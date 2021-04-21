import dash_core_components as dcc
import dash_html_components as html
from src.ui.callback import Callback
from dash.dependencies import Output, Input, State
import plotly.express as px


class HomeTemplate:
    _children: list = [
        html.Div('Population Modeling', className='header'),
        html.Div([
            html.Label('Choose type of selector',  className='label'),
            dcc.Dropdown(
                options=[
                    {'label': 'Uniform Selector', 'value': 'uniform'}
                ],
                value='uniform',
                id='selector',
                className='selector_dd'),
            html.Label('Choose level of aggressiveness of a selector', className='label'),
            dcc.Slider(
                max=1,
                min=0,
                marks={0: 'low', 0.5: 'medium', 1: 'high'},
                step=0.05,
                value=1,
                id='selector_value',
                className='slider_selector'
            ),
            html.Label('Choose type of mutator', className='label'),
            dcc.Dropdown(
                options=[
                    {'label': 'Normal Mutator', 'value': 'normal'}
                ],
                value='normal',
                id='mutator',
                className='mutator_dd'),
            html.Label('Choose level of variability of a mutator', className='label'),
            dcc.Slider(
                max=1,
                min=0,
                marks={0: 'low', 0.5: 'medium', 1: 'high'},
                step=0.05,
                value=0.5,
                id='mutator_value',
                className='slider_mutator'
            ),
            html.Label('Iterations: ', className='label'),
            dcc.Input(id='iterations', type='number', placeholder='number of iterations', value=3,
                      className='input_iter')
        ],
            className='population_params'
        ),

        html.Button('Build', id='build', n_clicks=0, className='build_button'),
        html.Button('Rebuild', id='rebuild', n_clicks=0, className='rebuild_button'),
        html.Div([html.Label('Maximum bacteria lifetime', className='label'),
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
                  html.Label('Death probability', className='label'),
                  dcc.Slider(
                      min=0,
                      max=1,
                      step=0.05,
                      marks={
                          0: '0',
                          1: '1'
                      },
                      value=0.5,
                      id='death'
                  ),
                  html.Label('Reproduction probability', className='label'),
                  dcc.Slider(
                      min=0,
                      max=1,
                      step=0.05,
                      marks={
                          0: '0',
                          1: '1'
                      },
                      value=0.5,
                      id='reproduction'),
                  html.Div(id='void'),
                  ],
                 className='bacteria_params',
                 ),
        html.Button('Add', id='add', n_clicks=0, className='add_button'),
        html.Div(id='output', children='Choose parameters', className='output_params'),
        html.Div('Population statistics visualization', className='graph_label'),
        html.Div([dcc.Graph(id='graph', figure=px.scatter(), className='graph')]),
        html.Div(id='hidden', children=[], style={'display': 'none'})]

    _callbacks: list = {'counter':
                            Callback((Output('output', 'children'),
                                      Input('death', 'value'),
                                      Input('reproduction', 'value')),
                                     {'prevent_initial_call': True}),

                        'add':
                            Callback((Output('void', 'children'),
                                      Input('add', 'n_clicks'),
                                      State('lifetime', 'value'),
                                      State('death', 'value'),
                                      State('reproduction', 'value')),
                                     {'prevent_initial_call': True}),

                        'build':
                            Callback((Output('graph', 'figure'),
                                      Input('build', 'n_clicks'),
                                      State('iterations', 'value'),
                                      State('selector', 'value'),
                                      State('selector_value', 'value'),
                                      State('mutator', 'value'),
                                      State('mutator_value', 'value')),
                                     {'prevent_initial_call': True}),

                        'rebuild':
                            Callback((Output('hidden', 'children'),
                                      Output('build', 'n_clicks'),
                                      Input('rebuild', 'n_clicks')),
                                     {'prevent_initial_call': True})
                        }

    @staticmethod
    def get_children():
        return HomeTemplate._children

    @staticmethod
    def get_callbacks():
        return HomeTemplate._callbacks
