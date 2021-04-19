from research.statistic import PopulationResearch
from src.population.species.bacteria.bacteria import create_bacteria
from src.population import Population
import plotly.express as px


stats = PopulationResearch()


def update_data(click_n):
    print('update_data')
    if click_n:
        print('update_data-1')
        stats = PopulationResearch(bacterias=[create_bacteria()])
        data = stats.research(click_n)
        print(data.to_json())
        return data.to_json()

    return '211111111111'


def update_graph(click_n):
    if click_n:
        stats = PopulationResearch(bacterias=[create_bacteria()])
        data = stats.research(click_n)

        return px.scatter(
            data
        )

    return px.scatter()


def update_output(n, death, reproduction):

    stats.research(n, statsParams(str, float, str, float)).data
    return "You've selected " + str(death) + " for death probability and " + str(reproduction) + \
           " for reproduction probability"


def add(n_clicks, lifetime, death, reproduction):
    print(n_clicks, lifetime, death, reproduction)
    if n_clicks is None:
        raise ["clicks " + str(n_clicks)]
    else:
        stats.add([create_bacteria(lifetime, death, reproduction)])
        return ["clicks " + str(n_clicks)]
