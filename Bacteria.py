from BacteriaParameters import BacteriaParameters
from EvolutionSimulator import EvolutionSimulator
from BacteriaGenome import BacteriaGenome


class Bacteria:
    """
       Represents bacteria with its parameters and ability for reproduction.

       Attributes
       ----------
       is_alive : bool
           Is bacteria alive or dead
       parameters :  BacteriaParameters
           Parameters of bacteria


       Methods
       -------
        iteration(self) -> list[Bacteria]
           In each iteration bacteria can die or can reproduct
       """

    def __init__(self, p: BacteriaParameters):
        self.is_alive = True
        self.parameters = p

    def iteration(self) -> list:

        """
        In method EvolutionSimulator decide fate of bactria: should it die or should it reproduct
        :return: list[Bacteria]
            List of child's if they are, if Bacteria not alive returns None
        """

        if not self.is_alive:
            return None
        else:
            if not EvolutionSimulator.have_to_die(self.parameters):
                children = list()
                while EvolutionSimulator.have_to_reproduct(self.parameters):
                    child_parameters = EvolutionSimulator.get_child_parameters(self.parameters)
                    children.append(Bacteria(child_parameters))
                self.parameters.lived_time += 1
                return children
            else:
                self.is_alive = False
                return []


def create_bacteria(population, max_life_time=5, p_for_death=0.5, p_for_reproduction=0.5) -> Bacteria:
    """
    Create bacteria from different parameters
    :param population: Population
        Population in which situated bacteria
    :param max_life_time: int
        Maximum iterations for bacteria
    :param p_for_death: float
        Probability of death
    :param p_for_reproduction: float
        Probability of reproduction
    :return: Bacteria
        Bacteria with set parameters
    """
    return Bacteria(BacteriaParameters(BacteriaGenome(max_life_time, p_for_death, p_for_reproduction), population))