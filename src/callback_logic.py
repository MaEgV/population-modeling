import functools
from dataclasses import dataclass, field
from typing import List
from research.statistic import PopulationResearch
from src.population.species.bacteria.bacteria import create_bacteria
from src.research.research_params import ResearchParams
import plotly.express as px


def storage(item):
    def real_storage(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            nonlocal item
            return func(item, *args, **kwargs)
        return inner

    return real_storage


@storage(PopulationResearch())
def research_storage(research, func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(research, *args, **kwargs)

    return inner


def update_output(death, reproduction):
    # stats.research(n, statsParams(str, float, str, float)).data
    return ["You've selected " + str(death) + " for death probability and " + str(reproduction) + \
           " for reproduction probability"]

@research_storage
def add(stats, n_clicks, lifetime, death, reproduction):
    stats.add_individuals([create_bacteria(lifetime, death, reproduction)])
    return ["added " + str(n_clicks)]

@research_storage
def build(stats, n_clicks, iterations, selector, selector_value, mutator, mutator_value):
    params = ResearchParams(selector, selector_value, mutator, mutator_value)
    result = stats.research(iterations, params)
    return [px.line(result.data)]
