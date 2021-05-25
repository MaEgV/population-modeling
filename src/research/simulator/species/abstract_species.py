from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List
from ..selectors.abstract_selector import AbstractSelector
from ..mutations.abstract_mutator import AbstractMutator
from ..genome import Genome


@dataclass # type: ignore
class AbstractSpecies:
    """
    Abstract class of an individual with genome that can reproduce and die

    Attributes
    ----------
    _genome: Genome
        An instance of the genome that will change over time
    Methods
    iterate(self, selector: AbstractSelector, mutator: AbstractMutator) -> List
        One iteration from the life of an individual, during which it can give offspring and die

    is_alive(self) -> bool
        Check state of the individual
    -------
    """
    _genome: Genome
    __id: int = field(default=0)

    @abstractmethod
    def produce_children(self, selector: AbstractSelector, mutator: AbstractMutator) -> List:
        """
        Randomly produces offspring. As a result-the offspring of an individual

        Parameters
        ----------
        selector: AbstractSelector
            Implementation of the selector that performs the evolution selection

        mutator: AbstractMutator
            Implementation of a mutator that determines genome variability and offspring

        Returns
        -------
            Children list
        """
        raise NotImplementedError

    @abstractmethod
    def evolve(self, selector: AbstractSelector, mutator: AbstractMutator) -> bool:
        """
        One life iteration. An individual change its state within this method

        Parameters
        ----------
        selector: AbstractSelector
            Implementation of the selector that performs the evolution selection

        mutator: AbstractMutator
            Implementation of a mutator that determines genome variability and offspring

        Returns
        -------
            Is alive
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Checking the status of the individual

        Returns
        -------
            Is the individual alive
        """
        raise NotImplementedError

    def get_id(self) -> int:
        return self.__id

    def set_id(self, new_id) -> None:
        self.__id = new_id

    def get_genome_dict(self) -> dict:
        return {'type': str(type(self)), 'max_life_time': self._genome.max_life_time, 'p_for_death': self._genome.p_for_death,
                'p_for_reproduction': self._genome.p_for_reproduction}
