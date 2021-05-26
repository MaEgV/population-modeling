from abc import abstractmethod
from dataclasses import dataclass
from src.research.simulator.genome import Genome


@dataclass
class SelectorParameters:
    """
    Dataclass for such mutational parameters as mean(loc) and standard deviation(scale).

    Attributes
    ----------
    loc: float
        Mean

    scale: float
        Standard deviation

    """
    loc: float
    scale: float


class AbstractSelector:
    """

    Simulate evolution processes. Decide what parameters should have child.

    Attributes
    ----------
    external_factors: ExternalFactors
        external factors affecting the life of bacteria

    have_to_die_funс:
        implementation of have to die logic

    have_to_reproduct_func:
        implementation of have to reproduce logic

    Methods
    -------
     __probability_parameter(parent_parameter: float) -> float
        Generate probability parameter based on parent's probability

    __choose_child_parameters(parent_parameters: BacteriaParameters) -> BacteriaParameters
        Create all child's parameters based on parent's probability

    have_to_die(p: BacteriaParameters) -> bool
        Decide should bacteria die or not

    have_to_reproduct(p: BacteriaParameters) -> bool
        Decide should bacteria reproduct or not

     get_child_parameters(p: BacteriaParameters) -> BacteriaParameters
        Return all child's parameters

    """

    @abstractmethod
    def is_died(self, genome: Genome) -> bool:
        raise NotImplementedError

    @abstractmethod
    def have_to_reproduce(self, genome: Genome) -> bool:
        raise NotImplementedError
