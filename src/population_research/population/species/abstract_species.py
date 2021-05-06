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
    def life_move(self, selector: AbstractSelector, mutator: AbstractMutator) -> List:
        """
        One life iteration. An individual can change its state within this method. As a result-the offspring of an individual

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


class Descendants:

    def __init__(self, child_species: list):
        self.__descendants: list = child_species

    def get_species(self) -> list:
        return self.__descendants

    def merge(self, new_descendants: list) -> list:
        few_descendants = self.__descendants
        for list_ in new_descendants:
            few_descendants += list_
        return few_descendants

    def get_bacterias_id(self):
        ids = list()
        for child in self.__descendants:
            ids.append(child.get_id())
        return ids


class Generation:

    def __init__(self, id: int, descendants: list):
        self.__id: int = id
        self.__generation: list = descendants

    def get_generation(self) -> list:
        return self.__generation

    def get_id(self) -> int:
        return self.__id

    def set_id(self, new_id):
        self.__id = new_id

    def get_bacterias_ids(self):
        ids = list()
        for descendants in self.__generation:
            ids.extend(descendants.get_bacterias_id())
        return ids
