from dataclasses import dataclass, field
from src.population import AbstractSelector, AbstractMutator, List, AbstractSpecies


@dataclass
class SimplePopulation:
    """
    A class that organizes the simple storage of individuals and allows them to reproduce and die

    Parameters
    ----------
    _individuals: list
        List with all individuals of population

    Methods
    -------
    iterate(self, selector: AbstractSelector, mutator: AbstractMutator) -> None
get_all(self)
get_alive(self)
get_dead(self)
    """
    _individuals: list = field(default_factory=list)

    def add(self, new_generation: list) -> None:
        """
        Wrapper for processing parent-child pairs.

        Attributes
        ----------
        population: SimplePopulation
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
        new_generation = _get_new_generation(self.get_alive(), selector, mutator)

        self._individuals.extend(new_generation)

    def get_all(self):
        """
        Returns the complete list of individuals

        Returns
        -------
        Full list of individuals
        """
        return self._individuals

    def get_alive(self):
        """
        Returns a list of live individuals only

        Returns
        -------
        Full list of individuals
        """
        return list(filter(lambda x: x.is_alive(), self._individuals))

    def get_dead(self):
        return list(filter(lambda x: not x.is_alive(), self._individuals))


def _get_new_generation(individuals: List[AbstractSpecies],
                        selector: AbstractSelector,
                        mutator: AbstractMutator) -> list:
    """
    Creates a new generation of individuals

    Parameters
    ----------
    individuals: List[AbstractSpecies]
        List of live individuals
    selector: AbstractSelector
        Selection operator
    mutator: AbstractMutator
        Mutation operator

    Returns
    -------
    list
    """
    new_generation = list()

    for individual in individuals:
        new_generation.extend(individual.iterate(selector, mutator))

    return new_generation