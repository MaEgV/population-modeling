from typing import Dict
from src.population_research.population.populations.simple_population import Population
import pandas as pd  # type: ignore
from dataclasses import dataclass, field
from src.population_research.research.parameters import IterationParameters, IndividualParameters


@dataclass(frozen=True)
class IterationResult:
    """
        The result of an evolutionary study of the population

        Attributes
        ----------
        id: int
            Research id
        data: pd.DataFrame
            Statistics collected at each iteration of the research
            Has columns defined in Stats and the number of rows equal to the number of iterations
        params: IterationParameters
            Parameters that were received as input
    """
    id: int
    data: pd.DataFrame
    parameters: IterationParameters


@dataclass(frozen=True)
class Researcher:
    """
        Class with some statistical tools for population analysis.

        Attributes
        ----------
        _population: Population
            An instance of the population that the study is being conducted on

        Methods
        -------
        build(self,
              num_iter: int,
              params: IterParams) -> IterRes
        Show number of species in population
    """
    _population: Population = field(default_factory=Population)

    def add_individual(self, parameters: IndividualParameters) -> None:
        self._population.add([parameters.get()])

    def build(self,
              iteration_number: int,
              parameters: IterationParameters) -> IterationResult:
        """
            Give data in DataFrame about population size and state on each iteration

            Attributes
            ----------
            iteration_number: int: Population
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
        frame = Stats.get_empty_frame()

        for _ in range(iteration_number):
            self._population.produce_new_generation(*parameters.get_params())
            frame = frame.append(Stats.get_statistic(self._population), ignore_index=True)

        return IterationResult(0, frame, parameters)

    def get_populations_size(self) -> int:
        return len(self._population.get_all())

    def drop(self) -> None:
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
    def get_statistic(population: Population) -> Dict[str, int]:
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
