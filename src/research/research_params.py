from dataclasses import dataclass, field
from typing import ClassVar
from src.population import AbstractSelector, AbstractMutator, SelectorParams, Bacteria, Genome, AbstractSpecies
from src.population import UniformSelector, NormalMutator
from src.population.mutations.mutator_parameters import MutatorParams


@dataclass(frozen=True)
class AvailableTypes:
    """
        The class contains an enumeration of all the types that can be used in the research

        Attributes
        ----------
        _selector_types: ClassVar[dict]

        _mutator_types: ClassVar[dict]

        Methods
        -------
        update(self, **kwargs) -> None
            Update genome parameters, which indicated in parameter 'params'
    """
    _selector_types: ClassVar[dict] = field(init=False, default={'uniform': UniformSelector})
    _mutator_types: ClassVar[dict] = field(init=False, default={'normal': NormalMutator})
    _individual_types: ClassVar[dict] = field(init=False, default={'bacteria': Bacteria})

    @staticmethod
    def get_selector_types():
        return list(AvailableTypes._selector_types.keys())

    @staticmethod
    def get_mutator_types():
        return list(AvailableTypes._mutator_types.keys())

    @staticmethod
    def get_individual_types():
        return list(AvailableTypes._individual_types.keys())

    @staticmethod
    def get_selector(key, init_params: SelectorParams) -> AbstractSelector:
        return AvailableTypes._selector_types[key](init_params)

    @staticmethod
    def get_mutator(key, init_params: MutatorParams) -> AbstractMutator:
        return AvailableTypes._mutator_types[key](init_params)

    @staticmethod
    def get_individual(key, init_params: Genome) -> AbstractSpecies:
        return AvailableTypes._individual_types[key](init_params)


class ParamsInfo:
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
class IterParams:
    selector: str
    selector_mode: float
    mutator: str
    mutator_mode: float

    def get_params(self):
        selector_params = SelectorParams(0, self.selector_mode)
        mutator_params = MutatorParams(0, self.mutator_mode)

        return (
            AvailableTypes.get_selector(self.selector, selector_params),
            AvailableTypes.get_mutator(self.mutator, mutator_params)
        )


@dataclass(frozen=True)
class AddParams:
    species: str
    lifetime: int
    p_for_death: float
    p_for_repr: float

    def get_params(self):
        return AvailableTypes.get_individual(self.species, Genome(self.lifetime, self.p_for_death, self.p_for_repr))
