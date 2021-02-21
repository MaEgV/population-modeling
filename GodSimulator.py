from random import random
import BacteriaParameters


class GodSimulator:

    @staticmethod
    def have_to_die(p: BacteriaParameters):
        if p.p_for_death > random():
            return True
        else:
            return False

    @staticmethod
    def have_to_reproduct(p: BacteriaParameters):
        if p.p_for_reproduction > random():
            return True
        else:
            return False

    @staticmethod
    def get_child_parameters(p: BacteriaParameters):
        return p
