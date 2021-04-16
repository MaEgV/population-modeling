from src.population.population import Population
from .selectors.bacterial_selector import AbstractSelector, UniformSelector, ExternalFactors
from .selectors.abstract_selector import SelectorParams
from .mutations.normal_mutator import AbstractMutator, NormalMutator
from src.population.individuals.bacteria import Bacteria


class LifeCycle:
    """
    Main cycle of the package with secondary iteration using the iterate method

    Parameters
    ----------
    population: Population
        Initial population

    Methods
    -------
    iterate(self, selectors: AbstractSelector, mutator: AbstractMutator, draw_func=lambda x: x) -> None
        Processes the possible descendants of all individuals in the population
    """
    def __init__(self, population: Population):
        self.population = population
        # TODO: Include external factors in this class

    def iterate(self, selector: AbstractSelector, mutator: AbstractMutator) -> None:
        """
        The time unit of evolution for a population. Processes a new generation in the population

        Parameters
        ----------
        selector: AbstractSelector
            Selection operator
        mutator: AbstractMutator
            Mutation operator
        draw_func: Callable
            Population rendering function

        Returns
        -------
        None
        """
        new_generation = self._get_new_generation(selector, mutator)

        self.population.add(new_generation)

    def _get_new_generation(
            self,
            selector: AbstractSelector,
            mutator: AbstractMutator) -> list:
        """
        Creates a new generation of individual

        Parameters
        ----------
        selector: AbstractSelector
            Selection operator
        mutator: AbstractMutator
            Mutation operator

        Returns
        -------
        list
        """
        new_generation = list()

        for individual in self.population.get_alive():
            if individual.is_alive():
                new_generation.extend(individual.cycle(selector, mutator))

        return new_generation



# def _update_properties(population: Population, selectors: AbstractSelector) -> None:
#     """
#     IN PROGRESS
#     Recounting external factors after iteration. Changing living conditions
#
#     Parameters
#     ----------
#     population: Population
#         Processed population
#
#     selectors: AbstractSelector
#         Required selectors
#
#     Returns
#     -------
#     None
#     """
#
#     selectors.external_factors.antagonism = 0  # TODO: add logic
#     selectors.external_factors.overpopulation = 0  # TODO: add logic
