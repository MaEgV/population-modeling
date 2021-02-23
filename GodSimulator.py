import copy
from random import uniform, random, randint
import BacteriaParameters


class GodSimulator:

    MAX_PROBABILITY = 1
    VARIATION_PROBABILITY_BORDERS = [-0.1, 0.1]
    LIVES_BORDERS = [0, 15]


    @staticmethod
    def __probability_parameter(parent_parameter: float) -> float:
        probability_variation = uniform(*VARIATION_PROBABILITY_BORDERS)
        parameter = parent_parameter + probability_variation
        if parameter > MAX_PROBABILITY:
            parameter = MAX_PROBABILITY
        return parameter

    @staticmethod
    def __choose_child_parameters(parent_parameters: BacteriaParameters) -> BacteriaParameters:
        child_parameters = copy.deepcopy(parent_parameters)
        child_parameters.genome.p_for_death = probability_parameter(parent_parameters.genome.p_for_death)
        child_parameters.genome.p_for_reproduction = probability_parameter(parent_parameters.genome.p_for_reproduction)
        child_parameters.genome.max_n = randint(*LIVES_BORDERS)
        return child_parameters

    @staticmethod
    def have_to_die(p: BacteriaParameters) -> bool:
        ratio = (p.genome.max_n - p.lived_time) / p.genome.max_n
        return p.p_for_death > uniform(0, ratio)

    @staticmethod
    def have_to_reproduct(p: BacteriaParameters) -> bool:
        return p.genome.p_for_reproduction > random()

    @staticmethod
    def get_child_parameters(p: BacteriaParameters) -> BacteriaParameters:
        return choose_child_parameters(p)
