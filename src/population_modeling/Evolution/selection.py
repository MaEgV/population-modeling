from src.population_modeling.Bacteria.genome import Genome
from src.population_modeling.Population import properties
from scipy.stats import uniform


class Selection:
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

    @staticmethod
    def have_to_die(genome: Genome, extend_factors: properties) -> bool:
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
        return extend_factors.antagonism + genome.p_for_death > uniform.rvs(0, 1)

    @staticmethod
    def have_to_reproduct(genome: Genome, extend_factors: properties) -> bool:
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
        return -extend_factors.overpopulation + genome.p_for_reproduction > uniform.rvs(0, 1)
