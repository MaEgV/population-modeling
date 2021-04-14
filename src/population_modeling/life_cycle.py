from src.population_modeling.population import Population
from .selector.selector import AbstractSelector, DefaultSelector, ExternalFactors
from .selector.selector_params import SelectorParams
from .mutations.normal_mutator import AbstractMutator, NormalMutator
from .bacteria import Bacteria


class LifeCycle:
    """
    Main cycle of the package with secondary iteration using the iterate method

    Parameters
    ----------
    population: Population
        Initial population

    Methods
    -------
    iterate(self, selector: AbstractSelector, mutator: AbstractMutator, draw_func=lambda x: x) -> None
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
            selector: AbstractSelector = DefaultSelector(SelectorParams(0,0.001), ExternalFactors(0, 0)),
            mutator: AbstractMutator = NormalMutator()) -> list:
        """
        Creates a new generation of bacteria

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

        for bacteria in self.population.individuals:

            if bacteria.is_alive():
                new_generation.extend(bacteria_cycle(bacteria, selector, mutator))

        return new_generation


def bacteria_cycle(bacteria: Bacteria, selector: AbstractSelector, mutator: AbstractMutator) -> list:
    """
    Life iteration of bacteria

    Parameters
    ----------
    bacteria: Bacteria
        Individual bacteria, witch is iterated
    selector: AbstractSelector
        Selection operator
    mutator: AbstractMutator
        Mutation operator

    Returns
    -------
    list
    """
    mutator.mutate(bacteria.genome)
    bacteria.inc_age()

    if selector.is_died(bacteria.genome):
        bacteria.die()
        return []
    
    return _parent_children(selector, mutator, bacteria)


def _parent_children(selector: AbstractSelector, mutation_mode: AbstractMutator, bacteria: Bacteria) -> list:
    """
    Generate bacteria's children

    Parameters
    ----------
    mutation_mode: AbstractMutator
        Implementation of mutation mechanisms

    bacteria: Bacteria
        A bacterium whose descendants may appear

    selector: AbstractSelector
        Make decisions about bacteria's future actions

    Returns
    -------
    list[Bacteria]
        Bacteria's children (if they are be)

    """

    children = list()
    while selector.have_to_reproduct(bacteria.genome):  # the Bernoulli test
        child_genome = mutation_mode.child_genome(bacteria.genome)
        children.append(Bacteria(child_genome))

    return children


# def _update_properties(population: Population, selector: AbstractSelector) -> None:
#     """
#     IN PROGRESS
#     Recounting external factors after iteration. Changing living conditions
#
#     Parameters
#     ----------
#     population: Population
#         Processed population
#
#     selector: AbstractSelector
#         Required selector
#
#     Returns
#     -------
#     None
#     """
#
#     selector.external_factors.antagonism = 0  # TODO: add logic
#     selector.external_factors.overpopulation = 0  # TODO: add logic
