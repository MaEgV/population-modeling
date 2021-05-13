from dataclasses import dataclass, field
from src.population_research.selectors.abstract_selector import AbstractSelector
from src.population_research.mutations.abstract_mutator import AbstractMutator

@dataclass
class Population:
    """
    A class that organizes the simple storage of individuals and allows them to reproduce and die

    Parameters
    ----------
    _individuals: list
        List with all individuals of population_research

    Methods
    -------
    iterate(self, selector: AbstractSelector, mutator: AbstractMutator) -> None

    get_all(self)

    get_alive(self)

    get_dead(self)

    drop(self)
    """
    _individuals: list = field(default_factory=list)
    __id: int = field(default=0)

    def add(self, new_generation: list) -> None:
        """
        Wrapper for processing parent-child pairs.

        Attributes
        ----------
        population_research: Population
            Processed population_research

        new_generation: list
            Contain pairs parent-children

        Returns
        -------
        None

        """
        self._individuals.extend(new_generation)

    def produce_new_generation(self, selector: AbstractSelector, mutator: AbstractMutator) -> None:
        """
        The time unit of evolution for a population_research. Processes a new generation in the population_research

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

    def get_id(self) -> int:
        return self.__id

    def set_id(self, new_id) -> None:
        self.__id = new_id

    def get_generations_ids(self) -> list:
        ids = set()
        for individual in self._individuals:
            ids.add(individual.get_id)

        return list(ids)

    def get_individual_ids(self) -> list:
        ids = list()
        for individual in self._individuals:
            ids.append(individual.get_id)
        return ids



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
