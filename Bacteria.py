import BacteriaParameters
from GodSimulator import GodSimulator


def create_child(p: BacteriaParameters):
    return Bacteria(p)


class Bacteria:

    def __init__(self, p: BacteriaParameters):
        self.is_alive = True
        self.parameters = p

    def iteration(self):
        children = list()
        child_parameters = GodSimulator.get_child_parameters(self.parameters)
        while child_parameters:
            children.append(create_child(child_parameters))
            child_parameters = GodSimulator.get_child_parameters(self.parameters)
        return children

