import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto


def home_page():
    return html.Div(
                    children=[
                        html.Button('Submit', id='button'),
                        html.Div(
                            children=dcc.Graph(
                                id="price-chart", config={"displayModeBar": False},
                            ),
                            className="card",
                        )
                        ]
                    )
