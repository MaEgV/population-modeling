from dataclasses import dataclass, field
from typing import ClassVar
from src.population_research.selectors.abstract_selector import AbstractSelector, SelectorParameters
from src.population_research.mutations.abstract_mutator import AbstractMutator
from src.population_research.species.bacteria.bacteria import Bacteria
from src.population_research.species.abstract_species import AbstractSpecies
from src.population_research.selectors.genomic_selector import UniformSelector
from src.population_research.mutations.normal_mutator import  NormalMutator
from src.population_research.mutations.mutator_parameters import MutatorParams
from src.population_research.genome import Genome

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
        get_selector_types() -> list:
            Possible types of selectors
        get_mutator_types() -> list:
            Possible types of mutators
        get_individual_types() -> list:
            Possible types of individuals
        get_selector(key, init_params: SelectorParams) -> AbstractSelector:
            Creates an instance of the selector by its key
        get_mutator(key, init_params: MutatorParams) -> AbstractMutator:
            Creates an instance of the mutator by its key
        get_individual(key, init_params: Genome) -> AbstractSpecies:
            Creates an instance of the individual by its key
    """
    _selector_types: ClassVar[dict] = field(init=False, default={'uniform': UniformSelector})
    _mutator_types: ClassVar[dict] = field(init=False, default={'normal': NormalMutator})
    _individual_types: ClassVar[dict] = field(init=False, default={'bacteria': Bacteria})

    @staticmethod
    def get_selector_types() -> list:
        return list(AvailableTypes._selector_types.keys())

    @staticmethod
    def get_mutator_types() -> list:
        return list(AvailableTypes._mutator_types.keys())

    @staticmethod
    def get_individual_types() -> list:
        return list(AvailableTypes._individual_types.keys())

    @staticmethod
    def get_selector(key: str, init_params: SelectorParameters) -> AbstractSelector:
        return AvailableTypes._selector_types[key](init_params)

    @staticmethod
    def get_mutator(key: str, init_params: MutatorParams) -> AbstractMutator:
        return AvailableTypes._mutator_types[key](init_params)

    @staticmethod
    def get_individual(key: str, init_params: Genome) -> AbstractSpecies:
        return AvailableTypes._individual_types[key](init_params)


# class ParametersInfo:
#     """
#     Contains static methods with information about entities from AvailableTypes
#     Methods
#     -------
#     get_selector_info() -> dict:
#         Dictionary about possible selectors
#     get_mutator_info() -> dict:
#         Dictionary about possible mutators
#     get_species_info() -> dict:
#         Dictionary about possible species
#     """
#     @staticmethod
#     def get_selector_info() -> dict:
#         return {
#             'Types': AvailableTypes.get_selector_types(),
#             'min': 0,  # TODO: move to SelectorParams
#             'max': 2
#         }
#
#     @staticmethod
#     def get_mutator_info() -> dict:
#         return {
#             'Types': list(AvailableTypes.get_mutator_types()),
#             'min': 0,  # TODO: move to MutatorParams
#             'max': 0.001
#         }
#
#     @staticmethod
#     def get_species_info() -> dict:
#         return {
#             'death_interval': (0, 1),  # TODO: move to ...
#             'reproduction_interval': (0, 1),
#             'lifetime_interval': (1, 20)
#         }


@dataclass(frozen=True)
class IterationParameters:
    """
    Date a class that stores parameters for adding an individual to the research population_research
    Attributes
    ----------
    selector: str
        Type of selector

    selector_mode: float
        Length of life of an individual

    mutator: str
        Type of mutator

    mutator_mode: float
        Probability of reproduction of an individual

    Methods
    -------
    get_params(self) -> AbstractSpecies:
        Returns an individual of the specified type
    """
    selector: str
    selector_mode: float
    mutator: str
    mutator_mode: float

    def get_params(self) -> tuple:
        selector_params = SelectorParameters(0, self.selector_mode)
        mutator_params = MutatorParams(0, self.mutator_mode)

        return (
            AvailableTypes.get_selector(self.selector, selector_params),
            AvailableTypes.get_mutator(self.mutator, mutator_params)
        )

    def get_dict(self) -> dict:
        return {'selector': self.selector, 'selector_mode': self.selector_mode, 'mutator': self.mutator,
                'mutator_mode': self.mutator_mode}


@dataclass(frozen=True)
class IndividualParameters:
    """
    Date a class that stores parameters for adding an individual to the research population_research
    Attributes
    ----------
    species: str
        Type of individual from AvailableTypes
    lifetime: int
        Length of life of an individual
    p_for_death: float
        Probability of death of an individual
    p_for_repr: float
        Probability of eproduction of an individual
    Methods
    -------
    get_params(self) -> AbstractSpecies:
        Returns an individual of the specified type
    """
    species: str
    lifetime: int
    p_for_death: float
    p_for_reproduction: float

    def get(self) -> AbstractSpecies:
        return AvailableTypes.get_individual(self.species, Genome(self.lifetime, self.p_for_death, self.p_for_reproduction))

    def get_dict(self) -> dict:
        return {'species': self.species, 'lifetime': self.lifetime, 'p_for_death': self.p_for_death,
                'p_for_reproduction': self.p_for_reproduction}
