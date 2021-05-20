from dataclasses import dataclass, field
from typing import List
import dash  # type: ignore
import requests
import plotly.express as px  # type: ignore
import pandas as pd  # type: ignore


@dataclass(frozen=True)
class ResearchApiUi:
    _research_url: str

    def add_individual(self,
                       add_clicks: int,
                       lifetime: int,
                       death: float,
                       reproduction: float) -> List[str]:
        """
        Adds an individual with the specified parameters to the population_research
        and returns the count of bacteria in the population_research

        Parameters
        ----------
        add_clicks: int
            Number of clicks on add
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

        # self._research.add_individual(IndividualParameters('bacteria', lifetime, death, reproduction))
        print(requests.post(
            self._research_url,
            json={"s": "bacteria",
                  "l": lifetime,
                  "p1": death,
                  "p2": reproduction}
        ))

        return [f"current population_research size:"]

    def build(self,
              build_clicks: int,
              n_iterations: int,
              selector_type: str,
              selector_value: float,
              mutator_type: str,
              mutator_value: float) -> list:
        """
        Conducts a statistical study of the evolution of the population_research

        Parameters
        ----------
        n_iterations: int
            The number of iterations with the specified parameters
        mutator_value: float
            Mutability value
        mutator_type: str
            Mutator type
        selector_value: float
            Selector aggressiveness
        selector_type: str
            Selector type
        build_clicks: int
            Number of clicks on build
        Returns
        -------
        List:
            I    print('BUILD', result.data)

        """
        parameters = IterationParameters(selector_type, selector_value, mutator_type, mutator_value)
        result = self._research.run(n_iterations, parameters)
        return [result.data.to_json(date_format='iso', orient='split')]

    # dataBase[addResearch, getResearch]

    def reset(self, n_clicks: int) -> list:
        """
        Erase data in the research
        Parameters
        ----------
        research
            A research instance from the global storage
        n_clicks
            ---
        Returns
        -------
            Trigger of recalculating dependencies
        """
        self._research.drop()
        return [
            pd.DataFrame.from_dict({'all': [0], 'alive': [0], 'dead': [0]}).to_json(date_format='iso', orient='split')]

    def get_callbacks_dict(self) -> dict:
        return {'selected_params_info': parameters_info,
                'add': lambda *args, **kwargs: self.add_individual(*args, **kwargs),
                'build': lambda *args, **kwargs: self.build(*args, **kwargs),
                'reset': lambda *args, **kwargs: self.reset(*args, **kwargs),
                'storage_update': storage_update,
                'figure_update': figure_update
                }


# TODO: remove magic constants
def parameters_info(death: float, reproduction: float) -> List[str]:
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


def storage_update(add_click: int,
                   build_storage: str,
                   reset_storage: str,
                   main_storage: str) -> list:
    """
    Function that updates the value of the global data store

    Parameters
    ----------
    add_click
    build_storage
        Build button storage
    reset_storage
        Rebuild button storage
    main_storage
         Main storage with dataframe

    Returns
    -------
        Updated value of the storage
    """
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[
        0]  # TODO: replace with timestamp check
    if main_storage:  # TODO: отдельная функция
        main_frame = pd.read_json(main_storage, orient='split')
        if 'add' == changed_id:
            main_frame.iloc[-1:, [0, 1]] += 1
        elif 'build_storage' == changed_id:
            new_frame = pd.read_json(build_storage, orient='split')
            main_frame = main_frame.append(new_frame, ignore_index=True)
        elif 'rebuild_storage' == changed_id:
            main_frame = pd.read_json(reset_storage, orient='split')
            print(main_frame)
        return [main_frame.to_json(date_format='iso', orient='split')]
    return [pd.DataFrame.from_dict({'all': [1], 'alive': [1], 'dead': [0]}).to_json(date_format='iso',
                                                                                    orient='split')]  # TODO: init


def figure_update(main_storage: str) -> list:
    """
    Redraws the graph every time the global storage is updated

    Parameters
    ----------
    main_storage
        Global storage with dataframe
    Returns
    -------
        Redrawn figure
    """
    main_frame = pd.read_json(main_storage, orient='split')
    return [px.bar(main_frame.loc[:, ['alive', 'dead']])]
