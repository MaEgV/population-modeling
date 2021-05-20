from dataclasses import dataclass, field
from src.population_research.simulator.selectors.abstract_selector import AbstractSelector
from src.population_research.simulator.mutations.abstract_mutator import AbstractMutator


@dataclass
class Generation:
    __id: int = field(default=0)
    __generation: list = field(default_factory=list)

    def get_species(self) -> list:
        return self.__generation

    def add_species(self, new_species: list):
        self.__generation.extend(new_species)

    def get_id(self) -> int:
        return self.__id

    def set_id(self, new_id):
        self.__id = new_id

    def get_bacterias_ids(self):
        ids = list()
        for descendants in self.__generation:
            ids.extend(descendants.get_bacterias_id())
        return ids


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

    def add_individuals(self, new_individuals: list) -> None:
        """
        Wrapper for processing parent-child pairs.

        Attributes
        ----------
        population_research: Population
            Processed population_research

        new_individuals: list
            Contain pairs parent-children

        Returns
        -------
        None

        """
        self._individuals.extend(new_individuals)

    def produce_new_generation(self, selector: AbstractSelector, mutator: AbstractMutator, evolve: bool = True) -> Generation:
        """
        The time unit of evolution for a population_research. Processes a new generation in the population_research

        Parameters
        ----------
        selector: AbstractSelector
            Selection operator
        mutator: AbstractMutator
            Mutation operator
        evolve: bool
            Do bacteria need to evolve

        Returns
        -------
        None
        """
        if evolve:
            for individual in self._individuals:
                if individual.is_alive():
                    individual.evolve(selector, mutator)

        new_generation = Generation()

        for individual in self._individuals:
            new_generation.add_species(individual.produce_children(selector, mutator))

        return new_generation

    def drop(self) -> None:
        """
        The method resets the list of stored individuals

        Returns
        -------
        None
        """
        self._individuals = list()

    def get_individuals(self) -> list:
        """
        Returns the complete list of individuals

        Returns
        -------
        Full list of individuals
        """
        return self._individuals

    def get_id(self) -> int:
        return self.__id

    def set_id(self, new_id) -> None:
        self.__id = new_id

    def get_individual_ids(self) -> dict:
        ids = dict()
        for individual in self._individuals:
            ids[str(individual.get_id())] = individual.get_id()
        return ids
