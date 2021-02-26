from src.population_modeling.Evolution.simulator import Simulator
from src.population_modeling.Evolution.genome import Genome
from src.population_modeling.Population.parameters import Parameters

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

    def __init__(self, p: Genome):
        self.is_alive = True
        self.genome = p

    def iteration(self, extend_factors: Parameters) -> list:

        """
        In method EvolutionSimulator decide fate of bactria: should it die or should it reproduct
        :return: list[Bacteria]
            List of child's if they are, if Bacteria not alive returns None
        """

        if not self.is_alive:
            raise BaseException('Addressing for a dead bacteria')
        else:
            if not Simulator.have_to_die(self.genome, extend_factors):
                children = list()
                while Simulator.have_to_reproduct(self.genome, extend_factors):
                    child_parameters = self.genome.child_genome()
                    children.append(Bacteria(child_parameters))
                return children
            else:
                self.is_alive = False
                return []


def create_bacteria(max_life_time=5, p_for_death=0.5, p_for_reproduction=0.5) -> Bacteria:
    """
    Create bacteria from different parameters
    :param max_life_time: int
        Maximum iterations for bacteria
    :param p_for_death: float
        Probability of death
    :param p_for_reproduction: float
        Probability of reproduction
    :return: Bacteria
        Bacteria with set parameters
    """
    return Bacteria(Genome(max_life_time, p_for_death, p_for_reproduction))
