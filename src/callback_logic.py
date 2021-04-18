from dash.exceptions import PreventUpdate

from research.statistic import Stats
from src.population.individuals.bacteria import create_bacteria
from src.population import Population
import plotly.express as px


population = Population()


def update_data(click_n):
    print('update_data')
    if click_n:
        print('update_data-1')
        stats = Stats(bacterias=[create_bacteria()])
        data = stats.research(click_n)
        print(data.to_json())
        return data.to_json()

    return '211111111111'


def update_graph(click_n):
    if click_n:
        stats = Stats(bacterias=[create_bacteria()])
        data = stats.research(click_n)

        return px.scatter(
            data
        )

    return px.scatter()


def update_output(death, reproduction):
    return "You've selected " + str(death) + " for death probability and " + str(reproduction) + \
           " for reproduction probability"


def add(n_clicks, lifetime, death, reproduction):
    print(n_clicks, lifetime, death, reproduction)
    if n_clicks is None:
        raise "clicks " + str(n_clicks)
    else:
        population.add([create_bacteria(lifetime, death, reproduction)])
        return "clicks " + str(n_clicks)
