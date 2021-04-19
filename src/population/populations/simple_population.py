from dataclasses import dataclass, field
from src.population import AbstractSelector, AbstractMutator


@dataclass
class Population:
    """
    A class containing information about the population. An iterator is implemented using a class Population.Iterator.
    Bacteria can get information about their population to adjust their behavior

    Parameters
    ----------
    genealogical_tree: igraph.Graph
        Structure of the population

    species: list
        List with all bacterias

    Methods
    -------
    draw(self, filename: str = None) -> None
        Drawing of population-graph
    """
    _individuals: list = field(default_factory=list)

    def add(self, new_generation: list) -> None:
        """
        Wrapper for processing parent-child pairs.

        Attributes
        ----------
        population: Population
            Processed population

        new_generation: list
            Contain pairs parent-children

        Returns
        -------
        None

        """
        self._individuals.extend(new_generation)

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

        self._individuals.extend(new_generation)

    def get_all(self):
        return self._individuals

    def get_alive(self):
        return list(filter(lambda x: x.is_alive(), self._individuals))

    def get_dead(self):
        return list(filter(lambda x: not x.is_alive(), self._individuals))



    def _get_new_generation(self,
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

        for individual in self.get_alive():
            new_generation.extend(individual.iterate(selector, mutator))

        return new_generation