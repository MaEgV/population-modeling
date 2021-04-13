from .abstract_callback import AbstractCallback
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State


class ButtonCallback(AbstractCallback):
    def __init__(self, function, params):
        super().__init__(params)
        self.function = function

    def get_function(self):
        def button(clicks, value):
            # Левый коллбэк
            if clicks:
                print(value, 'k9999')
                return html.Div(
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
            return {}
        return button
