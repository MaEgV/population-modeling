import dash_core_components as dcc

def example(clicks):
    print(2)
    if clicks:
        print(3)

    return dcc.Graph(id='graph')