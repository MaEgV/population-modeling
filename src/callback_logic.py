import functools
from research.population_research import Research
from src.research.research_params import IterParams, ParamsInfo, AddParams
import plotly.express as px


def storage(item):
    def real_storage(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            nonlocal item
            return func(item, *args, **kwargs)

        return inner

    return real_storage


@storage(Research())
def research_storage(research, func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(research, *args, **kwargs)

    return inner


def individual_counter(death, reproduction):
    return ["You've selected " + str(death) + " for death probability and " + str(reproduction) + \
            " for reproduction probability"]


@research_storage
def add(stats, n_clicks, lifetime, death, reproduction):
    stats.add_individual(AddParams('bacteria', lifetime, death, reproduction))

    return ["added " + str(n_clicks)]


@research_storage
def build(stats, n_clicks, iterations, selector, selector_value, mutator, mutator_value):
    # if n_clicks == 0:
    #     return [px.scatter()]
    params = IterParams(selector, selector_value, mutator, mutator_value)
    result = stats.research(iterations, params)
    return [px.line(result.data)]


@research_storage
def rebuild(stats, n_clicks):
    stats.drop()
    return [['0'], 0]


def selector_cfg(value):
    params = ParamsInfo.get_selector_info()
    types = params['Types']
    get_options = lambda value: {'label': value, 'value': value}
    options = list(map(get_options, types))
    marks = {params['min']: str(params['min']), params['max']: str(params['max'])}
    return options, options[0].get('value'), params['min'], params['max'], (params['max'] - params['min']) / 4, 1, marks


def mutator_cfg(value):
    params = ParamsInfo.get_mutator_info()
    types = params['Types']
    get_options = lambda value: {'label': value, 'value': value}
    options = list(map(get_options, types))
    marks = {params['min']: str(params['min']), params['max']: str(params['max'])}
    return options, options[0].get('value'), params['min'], params['max'], (params['max'] - params['min']) / 10, \
           0.0001, marks


def ndividual_cfg(value):
    species_info = ParamsInfo.get_species_info()
    get_marks = lambda value: (value, str(value))

    lifetime = species_info['lifetime_interval']
    lifetime_marks = dict(list(map(get_marks, range(lifetime[0], lifetime[1] + 1, 1))))

    death = species_info['death_interval']
    death_marks = dict(list(map(get_marks, death)))

    reproduction = species_info['reproduction_interval']
    reproduction_marks = dict(list(map(get_marks, reproduction)))

    return lifetime[0], lifetime[1], 1, lifetime_marks, 5, death[0], death[1], 0.1, death_marks, 0.5, \
           reproduction[0], reproduction[1], 0.1, reproduction_marks, 0.5
