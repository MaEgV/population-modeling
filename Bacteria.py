import BacteriaParameters
from GodSimulator import GodSimulator


def create_bacteria(**kwargs) -> Bacteria:
    return Bacteria(kwargs)


class Bacteria:

    def __init__(self, p: BacteriaParameters):
        self.is_alive = True
        self.parameters = p

    def iteration(self) -> list[Bacteria]:
        if not self.is_alive:
            return []
        else:
            if not GodSimulator.have_to_die(self.parameters):
                children = list()
                while GodSimulator.have_to_reproduct(self.parameters):
                    child_parameters = GodSimulator.get_child_parameters(self.parameters)
                    children.append(Bacteria(child_parameters))
                self.parameters.lived_time += 1
                return children
            else:
                self.is_alive = False
                return []
