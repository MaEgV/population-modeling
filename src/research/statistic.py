from copy import deepcopy
from dataclasses import dataclass, field
from typing import ClassVar, Dict
from src.population.mutations.mutator_parameters import MutatorParams
from src.population.population import Population
from src.population import AbstractSelector, NormalMutator, SelectorParams, UniformSelector
from src.population.life_cycle import LifeCycle
import pandas as pd


@dataclass
class ResearchParams:
    selector: str
    selector_mode: str
    mutator: str
    mutator_mode: str
    _selector_types: ClassVar = field(init=False, default={'uniform': UniformSelector})
    _selector_modes: ClassVar = field(init=False, default={'default': 1, 'cruel': 1.3, 'loyal': 0.5})
    _mutator_types: ClassVar = field(init=False, default={'normal': NormalMutator})
    _mutator_modes: ClassVar = field(init=False, default={'default': 0.01, 'high': 0.1, 'low': 0.005})

    def convert(self):
        selector_params = SelectorParams(0, ResearchParams._selector_modes[self.selector_mode])
        mutator_params = MutatorParams(0, ResearchParams._mutator_modes[self.mutator_mode])

        return (
            ResearchParams._selector_types[self.selector](selector_params),
            ResearchParams._mutator_types[self.mutator](mutator_params)
        )

    @staticmethod
    def get_modes():
        return {'Selector types': list(ResearchParams._selector_types.keys()),
                'Selector modes': list(ResearchParams._selector_modes.keys()),
                'Mutator types': list(ResearchParams._mutator_types.keys()),
                'Mutator modes': list(ResearchParams._mutator_modes.keys())}

@dataclass
class ResearchRes:
    id: int
    data: pd.DataFrame
    params: ResearchParams


def _get_stats(population: Population) -> Dict[str, int]:
    all_n, alive_n = len(population.get_all()), len(population.get_alive())
    dead_n = all_n - alive_n
    print({'all': all_n, 'alive': alive_n, 'dead': dead_n})
    return {'all': all_n, 'alive': alive_n, 'dead': dead_n}


class Stats:
    """
        Class with some statistical tools for population analysis.

        Attributes
        ----------
        cycle: LifeCycle
            Lifetime cycle of bacteria's population

        Methods
        -------
        num_of_individuals(self, num_iter: int, selectors: AbstractSelector, mutator: AbstractMutator,
                           draw_func) -> DataFrame
        Show number of individuals in population
    """

    def __init__(self, bacterias: list):
        self._bacterias = bacterias

    def research(self,
                 num_iter: int,
                 params: ResearchParams) -> ResearchRes:
        """
        Give data in DataFrame about population size and state on each iteration

        Attributes
        ----------
        num_iter: int: Population
            Number of supposed iterations

        selectors: AbstractSelector
            Chosen selectors for this population

        mutator: AbstractMutator
                Chosen mutator for this population

        Returns
        -------
        DataFrame
            Table with state of population on each iteration
        """
        population = Population(deepcopy(self._bacterias))
        cycle = LifeCycle(population)
        iter_params = params.convert()
        fr = pd.DataFrame(columns=['all', 'alive', 'dead'])

        for _ in range(num_iter):
            cycle.iterate(*iter_params)
            fr = fr.append(_get_stats(population), ignore_index=True)

        return ResearchRes(0, fr, params)
