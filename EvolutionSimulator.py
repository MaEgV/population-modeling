import copy
import BacteriaParameters
from scipy.stats import norm, uniform
from math import fabs


class EvolutionSimulator:
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

    max_probability = 1
    variation_probability_borders = [-0.1, 0.1]
    live_borders = [1, 15]


    @staticmethod
    def __probability_parameter(parent_parameter: float) -> float:
        """
        Generate random child's probability parameter based on parent's parameter
        :param parent_parameter: float
            parent's probability parameter: probability for death (p_for_death) or probability for reproduction
            (p_for_reproduction)
        :return: float
            child's probability parameter
        """
        probability_variation = norm.rvs(0, 0.01)
        parameter = fabs(parent_parameter + probability_variation)
        return parameter if parameter < EvolutionSimulator.max_probability else EvolutionSimulator.max_probability

    @staticmethod
    def __choose_child_parameters(parent_parameters: BacteriaParameters) -> BacteriaParameters:
        """
        Create all child's parameters (probability for death, probability for reproduction, max lifetime (max_live_time)
         based on parent's parameters
        :param parent_parameters: BacteriaParameters
            All parent's parameters
        :return:BacteriaParameters
            All child's parameters
        """
        child_parameters = copy.deepcopy(parent_parameters)
        child_parameters.genome.p_for_death = EvolutionSimulator.__probability_parameter(parent_parameters.genome.p_for_death)
        child_parameters.genome.p_for_reproduction = EvolutionSimulator.__probability_parameter(parent_parameters.genome.p_for_reproduction)
        child_parameters.genome.max_n = round(uniform.rvs(*EvolutionSimulator.live_borders))
        return child_parameters

    @staticmethod
    def have_to_die(p: BacteriaParameters) -> bool:
        """
        Decide if bacteria should die or not based on lifetime
        :param p: BacteriaParameters
            Bacteria's parameters
        :return: bool
            Decision: dead (true) or alive (false)
        """
        prob = uniform.rvs(0, 1)
        return p.genome.p_for_death > prob

    @staticmethod
    def have_to_reproduct(p: BacteriaParameters) -> bool:
        """
        Decide if bacteria should reproduct or not
        :param p: BacteriaParameters
            Bacteria's parameters
        :return:bool
            Decision: should reproduct (true) or shouldn't (false)
        """
        return p.genome.p_for_reproduction > uniform.rvs(0, 1)

    @staticmethod
    def get_child_parameters(p: BacteriaParameters) -> BacteriaParameters:
        """
        Put generated child parameters
        :param p: BacteriaParameters
            Bacteria's parameters
        :return: BacteriaParameters
            Child's parameters
        """
        return EvolutionSimulator.__choose_child_parameters(p)
