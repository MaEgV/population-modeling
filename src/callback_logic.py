from research.statistic import PopulationResearch
from src.population.species.bacteria.bacteria import create_bacteria
from src.population import Population
from src.research.research_params import ResearchParams

import plotly.express as px


stats = PopulationResearch()


def update_output(death, reproduction):
    # stats.research(n, statsParams(str, float, str, float)).data
    return ["You've selected " + str(death) + " for death probability and " + str(reproduction) + \
           " for reproduction probability"]


def add(n_clicks, lifetime, death, reproduction):
    print(n_clicks, lifetime, death, reproduction)
    stats.add_individuals([create_bacteria(lifetime, death, reproduction)])
    return ["added " + str(n_clicks)]


def build(n_clicks, iterations, selector, selector_value, mutator, mutator_value):
    params = ResearchParams(selector, selector_value, mutator, mutator_value)
    result = stats.research(iterations, params)
    print(result.data)
    return [px.line(result.data)]
