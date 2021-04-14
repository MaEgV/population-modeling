import json

import dash_core_components as dcc
from stats.statistic import PopulationStats
from population_modeling.bacteria import create_bacteria
import dash_html_components as html
import plotly.express as px
import pandas as pd

def update_data(click_n):
    print('update_data')
    if click_n:
        print('update_data-1')
        stats = PopulationStats(bacterias=[create_bacteria()])
        data = stats.num_of_individuals(click_n)
        print(data.to_json())
        return data.to_json()

    return '211111111111'


def update_graph(click_n):
    if click_n:
        stats = PopulationStats(bacterias=[create_bacteria()])
        data = stats.num_of_individuals(click_n)

        return px.scatter(
           data
        )

    return px.scatter()
