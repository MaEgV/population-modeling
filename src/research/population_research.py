from typing import Dict
from src.population.populations.simple_population import Population
from src.population import AbstractSelector, AbstractMutator
import pandas as pd
from dataclasses import dataclass, field
from src.research.research_params import IterParams, AddParams


@dataclass(frozen=True)
class IterRes:
    """
        The result of an evolutionary study of the population

        Attributes
        ----------
        id: int
            Research id
        data: pd.DataFrame
            Statistics collected at each iteration of the research
            Has columns defined in Stats and the number of rows equal to the number of iterations
        params: IterParams
            Parameters that were received as input
    """
    id: int
    data: pd.DataFrame
    params: IterParams


@dataclass(frozen=True)
class Research:
    """
        Class with some statistical tools for population analysis.

        Attributes
        ----------
        _population: Population
            An instance of the population that the study is being conducted on

        Methods
        -------
        research(self,
                 num_iter: int,
                 params: IterParams) -> IterRes

            Show number of species in population
    """
    _population: Population = field(default_factory=Population)

    def add_individual(self,
                       params: AddParams):
        self._population.add([params.get_params()])

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

    def get_populations_size(self):
        return len(self._population.get_all())

    def drop(self):
        self._population.drop()


class Stats:
    """
        A static class that collects statistics on a population instance

        Methods
        -------
        get_empty_frame() -> pd.DataFrame
            Returns an empty frame that can be filled with this class
            Can be used to define headers

        def get_stats(population: Population) -> Dict[str, int]:
            Collects statistics and returns a dictionary of results
    """
    @staticmethod
    def get_empty_frame() -> pd.DataFrame:
        """
            Returns an empty frame that can be filled with this class
            Can be used to define headers
        Returns
        -------
            pd.DataFrame
        """
        return pd.DataFrame(columns=['all', 'alive', 'dead'])

    @staticmethod
    def get_stats(population: Population) -> Dict[str, int]:
        """

        Parameters
        ----------
        population
            Instance of the population to be statistically examined

        Returns
        -------
        dict
            Results of stats research

        """
        all_n, alive_n = len(population.get_all()), len(population.get_alive())
        dead_n = all_n - alive_n

        return {'all': all_n, 'alive': alive_n, 'dead': dead_n}
