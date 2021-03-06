from typing import Dict
from research_app.research.simulator import Population
import pandas as pd  # type: ignore
from dataclasses import dataclass
from research_app.research.research import ResearchParameters


@dataclass(frozen=True)
class ResearchResult:
    """
        The result of an evolutionary study of the research

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
        Class with some statistical tools for research analysis.

        Attributes
        ----------
        _population: Population
            An instance of the research that the study is being conducted on

        Methods
        -------
        build(self,
              num_iter: int,
              params: IterParams) -> IterRes
        Show number of species in research
    """
    @staticmethod
    def run(population: Population,
            parameters: ResearchParameters) -> ResearchResult:
        """
            Give data in DataFrame about research size and state on each iteration

            Attributes
            ----------
            selectors: AbstractSelector
                Chosen selectors for this research

            mutator: AbstractMutator
                    Chosen mutator for this research

            Returns
            -------
            DataFrame
                Table with state of research on each iteration
        """
        df = Stats.get_empty_frame()

        for _ in range(parameters.iteration_number):
            population.add_individuals(population.produce_new_generation(*parameters.get_params()).get_species())
            df = df.append(Stats.get_statistic(population), ignore_index=True)

        return ResearchResult(0, df, parameters)


class Stats:
    """
        A static class that collects statistics on a research instance

        Methods
        -------
        get_empty_frame() -> pd.DataFrame
            Returns an empty frame that can be filled with this class
            Can be used to define headers

        def get_stats(research: Population) -> Dict[str, int]:
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
            Instance of the research to be statistically examined

        Returns
        -------
        dict
            Results of stats research

        """
        individuals = population.get_individuals()
        all_n = len(individuals)
        alive_n = len(list(filter(lambda x: x.is_alive(), individuals)))
        dead_n = all_n - alive_n

        return {'all': all_n, 'alive': alive_n, 'dead': dead_n}
