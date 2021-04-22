from typing import List, Tuple
import dash
from src.research.research_storage import research_storage, Research
from src.research.research_params import IterParams, ParamsInfo, AddParams
import plotly.express as px
import pandas as pd


def params_selected(death: float, reproduction: float) -> List[str]:
    """
    Displaying the selected parameters for the bacterium

    Parameters
    ----------
    death: float
        The value of the slider for the probability of death
    reproduction: float
        The value of the slider for the probability of reproduction
    Returns
    -------
        String for the label
    """
    return [f"You've selected {death} for death probability and {reproduction} for reproduction probability"]


@research_storage
def add(research: Research,
        add_clicks: int,
        build_clicks: int,
        lifetime: int,
        death: float,
        reproduction: float) -> List[str]:
    """
    Adds an individual with the specified parameters to the population
    and returns the count of bacteria in the population

    Parameters
    ----------
    research: Research
        A research instance from the global storage
    add_clicks: int
        Number of clicks on add
    build_clicks: int
        Number of clicks on build
    lifetime: int
        Life span of an individual
    death: float
        Probability of death of an individual per iteration
    reproduction: float
        Probability of reproduction of an individual per iteration
    Returns
    -------
    List[str]:
        Inscription
    """

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]  # TODO: replace with timestamp check

    if 'add' in changed_id:
        research.add_individual(AddParams('bacteria', lifetime, death, reproduction))

    return [f"current population size: {research.get_populations_size()}"]


@research_storage
def build(research: Research,
          n_clicks: int,
          iterations: int,
          selector: str,
          selector_value: float,
          mutator: str,
          mutator_value: float) -> list:

    params = IterParams(selector, selector_value, mutator, mutator_value)
    result = research.research(iterations, params)
    print('BUILD', result.data)
    return [result.data.to_json(date_format='iso', orient='split')]


@research_storage
def reset(stats, n_clicks):
    stats.drop()
    return [pd.DataFrame.from_dict({'all': [0], 'alive': [0], 'dead': [0]}).to_json(date_format='iso', orient='split')]


@research_storage
def storage_update(research, add_storage, build_storage, rebuild_storage, main_storage) -> list:
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]   # TODO: replace with timestamp check
    print(changed_id)
    if main_storage:
        main_frame = pd.read_json(main_storage, orient='split')
        if 'add' in changed_id:
            print(main_frame.iloc[-1:])
            main_frame.iloc[-1:, [0, 1]] += 1
        elif 'build_storage' in changed_id:
            new_frame = pd.read_json(build_storage, orient='split')
            main_frame = main_frame.append(new_frame, ignore_index=True)
        elif 'rebuild' in changed_id:
            main_frame = pd.read_json(rebuild_storage, orient='split')
        print('STORAGE', main_frame)

        return [main_frame.to_json(date_format='iso', orient='split')]
    return [pd.DataFrame.from_dict({'all': [1], 'alive': [1], 'dead': [0]}).to_json(date_format='iso', orient='split')]


def figure_update(main_storage):
    main_frame = pd.read_json(main_storage, orient='split')
    print('UPD', main_frame)

    return [px.line(main_frame)]