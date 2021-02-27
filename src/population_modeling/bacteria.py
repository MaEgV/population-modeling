from src.population_modeling.selector import Selector, Genome


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

    def iteration(self, selector: Selector) -> list:

        """
        In method EvolutionSimulator decide fate of bactria: should it die or should it reproduct
        :return: list[Bacteria]
            List of child's if they are, if Bacteria not alive returns None
        """
        if not self.is_alive:
            raise BaseException('Addressing for a dead bacteria')

        self.genome.spontaneous_mutation()

        if selector.have_to_die(self.genome):
            self.is_alive = False
            return []

        return self._get_children(selector)

    def _get_children(self, selector: Selector):
        children = list()
        while selector.have_to_reproduct(self.genome):  # the Bernoulli test
            child_parameters = self.genome.child_genome()
            children.append(Bacteria(child_parameters))

        return children


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