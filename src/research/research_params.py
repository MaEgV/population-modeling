from dataclasses import dataclass, field
from typing import ClassVar
from src.population import AbstractSelector, AbstractMutator, SelectorParams
from src.population import UniformSelector, NormalMutator
from src.population.mutations.mutator_parameters import MutatorParams
import pandas as pd


@dataclass(frozen=True)
class AvailableTypes:
    _selector_types: ClassVar = field(init=False, default={'uniform': UniformSelector})
    _mutator_types: ClassVar = field(init=False, default={'normal': NormalMutator})

    @staticmethod
    def get_selector_types():
        return list(AvailableTypes._selector_types.keys())

    @staticmethod
    def get_mutator_types():
        return list(AvailableTypes._mutator_types.keys())

    @staticmethod
    def get_selector(key, init_params: SelectorParams) -> AbstractSelector:
        return AvailableTypes._selector_types[key](init_params)

    @staticmethod
    def get_mutator(key, init_params: MutatorParams) -> AbstractMutator:
        return AvailableTypes._mutator_types[key](init_params)


@dataclass
class ResearchParams:
    selector: str
    selector_mode: float
    mutator: str
    mutator_mode: float

    def iter_params(self):
        selector_params = SelectorParams(0, self.selector_mode)
        mutator_params = MutatorParams(0, self.mutator_mode)

        return (
            AvailableTypes.get_selector(self.selector, selector_params),
            AvailableTypes.get_mutator(self.mutator, mutator_params)
        )

    @staticmethod
    def get_selector_info():
        return {
            'Types': AvailableTypes.get_selector_types(),
            'min': 0,  # TODO: move to SelectorParams
            'max': 2
        }

    @staticmethod
    def get_mutator_info():
        return {
            'Types': list(AvailableTypes.get_mutator_types()),
            'min': 0,  # TODO: move to MutatorParams
            'max': 1
        }

    @staticmethod
    def get_species_info():
        return {
            'death_interval': (0, 1),  # TODO: move to ...
            'repr_interval': (0, 1),
            'lifetime_interval': (1, 20)
        }


@dataclass(frozen=True)
class ResearchRes:
    id: int
    data: pd.DataFrame
    params: ResearchParams
