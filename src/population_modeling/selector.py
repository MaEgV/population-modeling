from src.population_modeling.genome import Genome
from scipy.stats import uniform, norm


class ExternalFactors:
    '''
    A class of population parameters that allows you to learn about the state of the population.
    With the help of this class of bacteria are able to control their size and composition.
    Play the role of external factors of evolution.
    '''
    def __init__(self, antagonism=0, overpopulation=0):
        self.antagonism = antagonism  # may be negative (collaboration)
        self.overpopulation = overpopulation


def default_have_to_die(ext_factors: ExternalFactors, genome: Genome):
    return ext_factors.antagonism + genome.p_for_death > uniform.rvs(0, 1)


def default_have_to_reproduct(ext_factors: ExternalFactors, genome: Genome):
    return -ext_factors.overpopulation + genome.p_for_reproduction > uniform.rvs(0, 1)


class Selector:
    """
    Simulate evolution processes. Decide what parameters should have child.

    Attributes
    ----------
    max_probability : int
        Maximum probability value
    variation_probability_borders : list[float]
        List of borders in which probability can variate
    live_borders : list[float]
        List of borders in which lifetime can variate

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
                 have_to_die_func=default_have_to_die,
                 have_to_reproduct_func=default_have_to_reproduct
                 ):
        self.have_to_die_func = have_to_die_func
        self.have_to_reproduct_func = have_to_reproduct_func
        self.external_factors = external_factors

    def have_to_die(self, genome: Genome) -> bool:
        """
        Decide if bacteria should die or not based on lifetime
        :param p: BacteriaParameters
            Bacteria's parameters
        :return: bool
            Decision: dead (true) or alive (false)

        Parameters
        ----------
        extend_factors
        genome
        """
        return self.have_to_die_func(self.external_factors, genome)

    def have_to_reproduct(self, genome: Genome) -> bool:
        """
        Decide if bacteria should reproduct or not
        :param p: BacteriaParameters
            Bacteria's parameters
        :return:bool
            Decision: should reproduct (true) or shouldn't (false)

        Parameters
        ----------
        extend_factors
        genome
        """
        return self.have_to_reproduct_func(self.external_factors, genome)

