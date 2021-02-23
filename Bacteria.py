import BacteriaParameters
from GodSimulator import GodSimulator


def create_child(p: BacteriaParameters):
    return Bacteria(p)


class Bacteria:

    def __init__(self, p: BacteriaParameters):
        self.is_alive = True
        self.parameters = p

    def iteration(self):
        if not self.is_alive:
            return None
        else:
            if not GodSimulator.have_to_die(self.parameters):
                children = list()
                while GodSimulator.have_to_reproduct(self.parameters):
                    child_parameters = GodSimulator.get_child_parameters(self.parameters)
                    children.append(create_child(child_parameters))
                self.parameters.lived_time += 1
                return children
            else:
                self.is_alive = False
                return None
