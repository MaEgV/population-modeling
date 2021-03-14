from population_modeling.selector import Genome


class Bacteria:
    """
       Represents bacteria with its parameters

       Attributes
       ----------
       is_alive : bool
           Is bacteria alive or dead

       genome : Genome
           Genome of bacteria

       Methods
       -------
        get_children(self, selector: Selector) -> list
            Generate children

       """

    def __init__(self, genome: Genome):
        self.is_alive = True
        self.age = 0
        self.genome = genome


def create_bacteria(
        max_life_time: int = 5,
        p_for_death: float = 0.5,
        p_for_reproduction: float = 0.5) -> Bacteria:
    """
    Create bacteria from different parameters

    Parameters
    ----------
    max_life_time: int
        Maximum iterations for bacteria

    p_for_death: float
        Probability of death

    p_for_reproduction: float
        Probability of reproduction

    Returns
    -------
    Bacteria
        Bacteria with set parameters

    """

    return Bacteria(Genome(max_life_time, p_for_death, p_for_reproduction))
