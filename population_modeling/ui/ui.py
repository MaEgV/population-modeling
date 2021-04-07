import dash
import dash_core_components as dcc
import dash_html_components as html
from pandas import DataFrame
import numpy as np
from dash.dependencies import Output, Input, State



external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
storage = dict()


class DashUI:
    def __init__(self, callbacks: dict):
        app.title = "Avocado Analytics: Understand Your Avocados!"
        app.layout = html.Div()
        global storage
        storage = callbacks
        app.layout = html.Div(
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
        app.run_server(debug=True, host='127.0.0.1')





@app.callback(
    Output('price-chart', 'figure'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')])
def button(n_clicks, value):
    print(2)
    if n_clicks:
        data = storage['button'](n_clicks, value)
        return {
            "data": [
                {
                    "x": data["iterations"],
                    "y": data["number_of_individuals"],
                    "type": "lines",
                    "hovertemplate": "$%{y:.2f}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "Average Price of Avocados",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {"tickprefix": "$", "fixedrange": True},
                "colorway": ["#17B897"],
            },
        }
    return {}



# if __name__ == "__main__":
#     app.run_server(debug=True,
#                    host='127.0.0.1')