from random import random
import BacteriaParameters


class GodSimulator:

    @staticmethod
    def have_to_die(p: BacteriaParameters):
        return p.p_for_death > random()

    @staticmethod
    def have_to_reproduct(p: BacteriaParameters):
        return p.p_for_reproduction > random()

    @staticmethod
    def get_child_parameters(p: BacteriaParameters):
        return p
