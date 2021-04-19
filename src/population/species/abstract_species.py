from abc import abstractmethod
from dataclasses import dataclass
from typing import List
from ..selectors.abstract_selector import AbstractSelector
from ..mutations.abstract_mutator import AbstractMutator
from src.population import Genome


@dataclass(frozen=True)
class AbstractSpecies:
    _genome: Genome

    @abstractmethod
    def iterate(self, selector: AbstractSelector, mutator: AbstractMutator) -> List:
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        raise NotImplementedError
