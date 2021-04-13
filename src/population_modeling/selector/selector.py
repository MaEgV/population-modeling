from ..genome import Genome
from scipy.stats import uniform  # type: ignore
from abc import abstractmethod
from ..selector.selector_params import SelectorParams


class ExternalFactors:
    """

    A class of population parameters that allows you to learn about the state of the population.

    With the help of this class of bacteria are able to control their size and composition.
    Play the role of external factors of evolution.

    Attributes
    ----------
    antagonism : float
        External factor which increases death probability

    overpopulation : float
        Degree of overcrowding. Influence on reproduction probability.

    """

    def __init__(self, antagonism: float = 0, overpopulation: float = 0):
        self.antagonism = antagonism  # may be negative (collaboration)
        self.overpopulation = overpopulation


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
    def have_to_reproduct(self, genome: Genome) -> bool:
        raise NotImplementedError


class DefaultSelector(AbstractSelector):
    def __init__(self,
                 params: SelectorParams,
                 ext_factors: ExternalFactors):
        self.params = params
        self.ext_factors = ext_factors

    def is_died(self, genome: Genome) -> bool:
        """

        Decide if bacteria should die or not based on lifetime

        Parameters
        ----------
        genome: Genome
            Bacteria's genome

        Returns
        -------
        bool
            Decision: dead (true) or alive (false)
        """
        return self.ext_factors.overpopulation + genome.p_for_death > \
               uniform.rvs(self.params.loc, self.params.scale)

    def have_to_reproduct(self, genome: Genome) -> bool:
        """

        Decide if bacteria should reproduct or not

        Parameters
        ----------
        genome: Genome
            Bacteria's genome

        Returns
        -------
        bool
            Decision: should reproduct (true) or shouldn't (false)
        """
        return -self.ext_factors.overpopulation + genome.p_for_reproduction > \
               uniform.rvs(self.params.loc, self.params.scale)
