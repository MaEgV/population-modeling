from population_modeling.genome import Genome
from scipy.stats import uniform, norm  # type: ignore
from typing import Callable


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


def default_have_to_die(ext_factors: ExternalFactors, genome: Genome) -> bool:
    """

    Default way to decide should bacteria die or not.

    Parameters
    ----------
    ext_factors: ExternalFactors
        External bacteria's factors

    genome: Genome
        Bacteria's genome

    Returns
    -------
    bool
        Deciding whether bacteria should die
    """
    return ext_factors.antagonism + genome.p_for_death > uniform.rvs(0, 1)


def default_have_to_reproduct(ext_factors: ExternalFactors, genome: Genome) -> bool:
    """

    Default way to decide should bacteria reproduct or not.

    Parameters
    ----------
    ext_factors: ExternalFactors
        External bacteria's factors

    genome: Genome
        Bacteria's genome

    Returns
    -------
    bool
        Deciding whether bacteria should reproduct
    """
    return -ext_factors.overpopulation + genome.p_for_reproduction > uniform.rvs(0, 1)


class Selector:
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

    def __init__(self,
                 external_factors: ExternalFactors,
                 have_to_die_func: Callable = default_have_to_die,
                 have_to_reproduct_func: Callable = default_have_to_reproduct
                 ):
        self.have_to_die_func = have_to_die_func
        self.have_to_reproduct_func = have_to_reproduct_func
        self.external_factors = external_factors

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
        return self.have_to_die_func(self.external_factors, genome)

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
        return self.have_to_reproduct_func(self.external_factors, genome)
