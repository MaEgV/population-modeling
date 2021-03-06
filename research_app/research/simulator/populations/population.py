from dataclasses import dataclass, field
from typing import List

from research_app.research.simulator import AbstractSelector  # type: ignore
from research_app.research.simulator import AbstractMutator  # type: ignore


@dataclass
class Generation:
    __id: int = field(default=0)
    __generation: list = field(default_factory=list)

    def get_species(self) -> list:
        return self.__generation

    def add_species(self, new_species: list) -> None:
        self.__generation.extend(new_species)

    def get_id(self) -> int:
        return self.__id

    def set_id(self, new_id: int) -> None:
        self.__id = new_id

    def get_bacterias_ids(self) -> list:
        ids: List[int] = list()
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
        List with all individuals of research

    Methods
    -------
    iterate(self, selector: AbstractSelector, mutator: AbstractMutator) -> None

    get_all(self)

    get_alive(self)

    get_dead(self)

    drop(self)
    """
    _individuals: list = field(default_factory=list)

    def add_individuals(self, new_individuals: list) -> None:
        """
        Wrapper for processing parent-child pairs.

        Attributes
        ----------
        research: Population
            Processed research

        new_individuals: list
            Contain pairs parent-children

        Returns
        -------
        None

        """
        self._individuals.extend(new_individuals)

    def produce_new_generation(self, selector: AbstractSelector, mutator: AbstractMutator,
                               evolve: bool = True) -> Generation:
        """
        The time unit of evolution for a research. Processes a new generation in the research

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
        counter = 0
        new_generation = Generation()
        if evolve:
            for individual in self._individuals:
                if individual.is_alive() and individual.evolve(selector, mutator):
                    new_generation.add_species(individual.produce_children(selector, mutator))
                    counter += 1
                    if counter > 1700:
                        return new_generation
        else:
            for individual in list(filter(lambda x: x.is_alive(), self._individuals)):
                new_generation.add_species(individual.produce_children(selector, mutator))
        print('evolve3', new_generation)
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

    def set_id(self, new_id: int) -> None:
        self.__id = new_id

    def get_individual_ids(self) -> dict:
        ids = dict()
        for individual in self._individuals:
            ids[str(individual.get_id())] = individual.get_id()
        return ids
