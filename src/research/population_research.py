from typing import Dict
from src.population.populations.simple_population import SimplePopulation
from src.population import AbstractSelector, AbstractMutator
import pandas as pd
from dataclasses import dataclass, field
from src.research.research_params import IterParams, AddParams


@dataclass(frozen=True)
class IterRes:
    id: int
    data: pd.DataFrame
    params: IterParams


@dataclass(frozen=True)
class Researcher:
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
        Show number of species in population
    """
    _population: SimplePopulation = field(default_factory=SimplePopulation)

    def add_individuals(self,
                        params: AddParams):
        self._population.add(*params.get_params())

    def research(self,
                 num_iter: int,
                 params: IterParams) -> IterRes:
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
        fr = Stats.get_empty_frame()

        for _ in range(num_iter):
            self._population.iterate(*params.get_params())
            fr = fr.append(Stats.get_stats(self._population), ignore_index=True)

        return IterRes(0, fr, params)


class Stats:
    @staticmethod
    def get_empty_frame():
        return pd.DataFrame(columns=['all', 'alive', 'dead'])

    @staticmethod
    def get_stats(population: SimplePopulation) -> Dict[str, int]:
        all_n, alive_n = len(population.get_all()), len(population.get_alive())
        dead_n = all_n - alive_n

        return {'all': all_n, 'alive': alive_n, 'dead': dead_n}
