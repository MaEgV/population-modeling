from research.statistic import Stats
from src.population.individuals.bacteria import create_bacteria
import plotly.express as px


def update_data(click_n):
    print('update_data')
    if click_n:
        print('update_data-1')
        stats = Stats(bacterias=[create_bacteria()])
        data = stats.num_of_individuals(click_n)
        print(data.to_json())
        return data.to_json()

    return '211111111111'


def update_graph(click_n):
    if click_n:
        stats = Stats(bacterias=[create_bacteria()])
        data = stats.num_of_individuals(click_n)

        return px.scatter(
           data
        )

    return px.scatter()
