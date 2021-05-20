from typing import Dict
from src.population_research.simulator import Population
import pandas as pd  # type: ignore
from dataclasses import dataclass, field
from src.population_research.research.parameters import ResearchParameters, IndividualParameters


@dataclass(frozen=True)
class IterationResult:
    """
        The result of an evolutionary study of the population_research

        Attributes
        ----------
        id: int
            Research id
        data: pd.DataFrame
            Statistics collected at each iteration of the research
            Has columns defined in Stats and the number of rows equal to the number of iterations
        params: ResearchParameters
            Parameters that were received as input
    """
    id: int
    data: pd.DataFrame
    parameters: ResearchParameters


@dataclass(frozen=True)
class Research:
    """
        Class with some statistical tools for population_research analysis.

        Attributes
        ----------
        _population: Population
            An instance of the population_research that the study is being conducted on

        Methods
        -------
        build(self,
              num_iter: int,
              params: IterParams) -> IterRes
        Show number of species in population_research
    """
    @staticmethod
    def run(population,
            parameters: ResearchParameters) -> IterationResult:
        """
            Give data in DataFrame about population_research size and state on each iteration

            Attributes
            ----------
            selectors: AbstractSelector
                Chosen selectors for this population_research

            mutator: AbstractMutator
                    Chosen mutator for this population_research

            Returns
            -------
            DataFrame
                Table with state of population_research on each iteration
        """
        df = Stats.get_empty_frame()

        for _ in range(parameters.iteration_number):
            population.add_individuals(population.produce_new_generation(*parameters.get_params()).get_species())
            df = df.append(Stats.get_statistic(population), ignore_index=True)

        return IterationResult(0, df, parameters)


class Stats:
    """
        A static class that collects statistics on a population_research instance

        Methods
        -------
        get_empty_frame() -> pd.DataFrame
            Returns an empty frame that can be filled with this class
            Can be used to define headers

        def get_stats(population_research: Population) -> Dict[str, int]:
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
            Instance of the population_research to be statistically examined

        Returns
        -------
        dict
            Results of stats research

        """
        all_n = len(population.get_individuals())
        dead_n = all_n - 0

        return {'all': all_n, 'alive': 0, 'dead': dead_n}
