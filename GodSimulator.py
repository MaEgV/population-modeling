import copy
from random import uniform, random, randint
import BacteriaParameters


def probability_parameter(parent_parameter: float):
    probability_variation = uniform(-0.1, 0.1)
    parameter = parent_parameter + probability_variation
    if parameter > 1:
        parameter = 1
    return parameter


def choose_child_parameters(parent_parameters: BacteriaParameters):
    child_parameters = copy.deepcopy(parent_parameters)
    child_parameters.genome.p_for_death = probability_parameter(parent_parameters.genome.p_for_death)
    child_parameters.genome.p_for_reproduction = probability_parameter(parent_parameters.genome.p_for_reproduction)
    child_parameters.genome.max_n = randint(0, 15)
    return child_parameters


class GodSimulator:

    @staticmethod
    def have_to_die(p: BacteriaParameters):
        ratio = (p.genome.max_n - p.lived_time) / p.genome.max_n
        return p.p_for_death > uniform(0, ratio)

    @staticmethod
    def have_to_reproduct(p: BacteriaParameters):
        return p.genome.p_for_reproduction > random()

    @staticmethod
    def get_child_parameters(p: BacteriaParameters):
        return choose_child_parameters(p)
