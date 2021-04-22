import dash_core_components as dcc  # type: ignore
import dash_html_components as html  # type: ignore
from src.ui.callback import Callback
from dash.dependencies import Output, Input, State  # type: ignore
import plotly.express as px  # type: ignore


individual_dropdown_init = {
    'options': [{'label': 'Bacteria', 'value': 'bacteria'}],
    'value': 'bacteria',
    'className': 'dd'
}
selector_dropdown_init = {
    'options': [{'label': 'Uniform Selector', 'value': 'uniform'}],
    'value': 'uniform',
    'className': 'dd'
}
selector_slider_init = {
    'max': 0.9,
    'min': 0.1,
    'marks': {0.1: 'low', 0.5: 'medium', 0.9: 'high'},
    'step': 0.05,
    'value': 0.5,
    'className': 'slider_selector'
}
mutator_dropdown_init = {
    'options': [{'label': 'Normal Mutator', 'value': 'normal'}],
    'value': 'normal',
    'className': 'dd'
}
mutator_slider_init = {
    'max': 0.2,
    'min': 0,
    'marks': {0: 'low', 0.5: 'medium', 1: 'high'},
    'step': 0.01,
    'value': 0.1,
    'className': 'slider_mutator'
}
input_iter_init = {
    'type': 'number',
    'placeholder': 'number of iterations',
    'value': 1,
    'className': 'input_iter'
}
lifetime_slider_init = {
    'max': 10,
    'min': 1,
    'marks': {1: '1',
              2: '2',
              3: '3',
              4: '4',
              5: '5',
              6: '6',
              7: '7',
              8: '8',
              9: '9',
              10: '10'},
    'step': 1,
    'value': 5,
    'className': 'lifetime'
}
death_slider_init = {
    'max': 1,
    'min': 0,
    'marks': {0: 'low', 0.5: 'medium', 1: 'high'},
    'step': 0.05,
    'value': 0.5,
}
repr_slider_init = {
    'max': 1,
    'min': 0,
    'marks': {0: 'low', 0.5: 'medium', 1: 'high'},
    'step': 0.05,
    'value': 0.5,
}


class HomeTemplate:
    """


        Attributes
        ----------
        _population: Population
            An instance of the population that the study is being conducted on

        Methods
        -------
    """
    _children: list = [
        html.Div('Population Modeling', className='header'),
        html.Div([
            html.Label('Choose type of selector', className='label'),
            dcc.Dropdown(id='selector', **selector_dropdown_init),

            html.Label('Choose level of aggressiveness of a selector', className='label'),
            dcc.Slider(id='selector_value', **selector_slider_init),

            html.Label('Choose type of mutator', className='label'),
            dcc.Dropdown(id='mutator', **mutator_dropdown_init),

            html.Label('Choose level of variability of a mutator', className='label'),
            dcc.Slider(id='mutator_value', **mutator_slider_init),

            html.Label('Iterations: ', className='label'),
            dcc.Input(id='iterations', **input_iter_init)
        ],
            className='population_params'
        ),

        html.Button('Build', id='build', n_clicks=0, className='build_button'),
        html.Div(id='build_storage', style={'display': 'none'}),

        html.Button('Rebuild', id='rebuild', n_clicks=0, className='rebuild_button'),
        html.Div(id='rebuild_storage', style={'display': 'none'}),

        html.Div([
            html.Label('Choose type of individual', className='label'),
            dcc.Dropdown(id='individual', **individual_dropdown_init),

            html.Label('Maximum bacteria lifetime', className='label'),
            dcc.Slider(id='lifetime', **lifetime_slider_init),

            html.Label('Death probability', className='label'),
            dcc.Slider(id='death', **death_slider_init),

            html.Label('Reproduction probability', className='label'),
            dcc.Slider(id='reproduction', **repr_slider_init),
        ],
            className='bacteria_params',
        ),
        html.Button('Add', id='add', n_clicks=0, className='add_button'),
        html.Div(id='add_storage', style={'display': 'none'}),
        html.Div(id='counter', children=['0']),
        html.Div(id='output', children='Choose parameters', className='output_params'),
        html.Div('Population statistics visualization', className='graph_label'),
        html.Div([dcc.Graph(id='graph', figure=px.scatter(), className='graph')]),
        html.Div(id='hidden', style={'display': 'none'})]

    _callbacks: dict = {'params_selected':
                            Callback((Output('output', 'children'),
                                      Input('death', 'value'),
                                      Input('reproduction', 'value')),
                                     {'prevent_initial_call': True}),

                        'add':
                            Callback((Output('counter', 'children'),
                                      Input('add', 'n_clicks'),
                                      Input('build', 'n_clicks'),
                                      State('lifetime', 'value'),
                                      State('death', 'value'),
                                      State('reproduction', 'value')),
                                     {'prevent_initial_call': True}),

                        'build':
                            Callback((Output('build_storage', 'children'),
                                      Input('build', 'n_clicks'),
                                      State('iterations', 'value'),
                                      State('selector', 'value'),
                                      State('selector_value', 'value'),
                                      State('mutator', 'value'),
                                      State('mutator_value', 'value')),
                                     {'prevent_initial_call': True}),

                        'reset':
                            Callback((Output('rebuild_storage', 'children'),
                                      Input('rebuild', 'n_clicks')),
                                     {'prevent_initial_call': True}),

                        'storage_update':
                            Callback((Output('hidden', 'children'),
                                      Input('add', 'n_clicks'),
                                      Input('build_storage', 'children'),
                                      Input('rebuild_storage', 'children'),
                                      State('hidden', 'children')),
                                     {'prevent_initial_call': True}),

                        'figure_update':
                            Callback((Output('graph', 'figure'),
                                      Input('hidden', 'children')),
                                     {'prevent_initial_call': True})}

    @staticmethod
    def get_children() -> list:
        return HomeTemplate._children

    @staticmethod
    def get_callbacks() -> dict:
        return HomeTemplate._callbacks
