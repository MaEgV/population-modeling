from dataclasses import dataclass, field
from src.population_research.population import AbstractSelector, AbstractMutator

@dataclass
class Population:
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

    drop(self)
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

    def produce_new_generation(self, selector: AbstractSelector, mutator: AbstractMutator) -> None:
        """
        The time unit of evolution for a population. Processes a new generation in the population

        Parameters
        ----------
        selector: AbstractSelector
            Selection operator
        mutator: AbstractMutator
            Mutation operator

        Returns
        -------
        None
        """
        new_generation = _get_new_generation(self.get_alive(), selector, mutator)

        self._individuals.extend(new_generation)

    def get_all(self) -> list:
        """
        Returns the complete list of individuals

        Returns
        -------
        Full list of individuals
        """
        return self._individuals

    def get_alive(self) -> list:
        """
        Returns a list of alive individuals only

        Returns
        -------
        Full list of individuals
        """
        return list(filter(lambda x: x.is_alive(), self._individuals))

    def get_dead(self) -> list:
        """
        Returns a list of dead individuals only

        Returns
        -------
        Full list of individuals
        """
        return list(filter(lambda x: not x.is_alive(), self._individuals))

    def drop(self) -> None:
        """
        The method resets the list of stored individuals

        Returns
        -------
        None
        """
        self._individuals = list()


def _get_new_generation(individuals: list,
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
        descendants = individual.life_move(selector, mutator)
        new_generation.extend(descendants.get_species())

    return new_generation
