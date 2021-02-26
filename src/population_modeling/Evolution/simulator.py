from src.population_modeling.Bacteria.parameters import Parameters
from src.population_modeling.Evolution.genome import Genome, MutationalProcesses, NormalMutations
from scipy.stats import uniform


class Simulator:
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
    mutations_mode: MutationalProcesses = NormalMutations()

    @staticmethod
    def __choose_child_parameters(parent_parameters: Parameters) -> Parameters:
        """
        Create all child's parameters (probability for death, probability for reproduction, max lifetime (max_live_time)
         based on parent's parameters
        :param parent_parameters: BacteriaParameters
            All parent's parameters
        :return:BacteriaParameters
            All child's parameters
        """
        child_genome = Genome(
            Simulator.mutations_mode.child_max_n(parent_parameters.genome),
            Simulator.mutations_mode.child_p_for_death(parent_parameters.genome),
            Simulator.mutations_mode.child_p_for_reproduction(parent_parameters.genome)
        )

        return Parameters(child_genome, parent_parameters.population)

    @staticmethod
    def have_to_die(p: Parameters) -> bool:
        """
        Decide if bacteria should die or not based on lifetime
        :param p: BacteriaParameters
            Bacteria's parameters
        :return: bool
            Decision: dead (true) or alive (false)
        """
        extend_factors = p.population.p.antagonism

        return extend_factors + p.genome.p_for_death > uniform.rvs(0, 1)

    @staticmethod
    def have_to_reproduct(p: Parameters) -> bool:
        """
        Decide if bacteria should reproduct or not
        :param p: BacteriaParameters
            Bacteria's parameters
        :return:bool
            Decision: should reproduct (true) or shouldn't (false)
        """
        extend_factors = p.population.p.overpopulation

        return extend_factors + p.genome.p_for_reproduction > uniform.rvs(0, 1)

    @staticmethod
    def get_child_parameters(p: Parameters) -> Parameters:
        """
        Put generated child parameters
        :param p: BacteriaParameters
            Bacteria's parameters
        :return: BacteriaParameters
            Child's parameters
        """
        return Simulator.__choose_child_parameters(p)
