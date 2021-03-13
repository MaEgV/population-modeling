class Genome:
    """

    Class for description of bacteria's genome.

    Attributes
    ----------
    max_life_time : int
        Maximum iterations for bacteria

    p_for_death : float
        Probability of death

    p_for_reproduction : float
        Probability of reproduction

    Methods
    -------
    child_genome(self) -> Genome
        Returns generated child's genome

    """

    def __init__(self, max_life_time_: int, p_for_death_: float, p_for_reproduction_: float):
        self.max_life_time = max_life_time_
        self.p_for_death = p_for_death_
        self.p_for_reproduction = p_for_reproduction_
