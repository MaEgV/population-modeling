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

    """

    def __init__(self, max_life_time: int, p_for_death: float, p_for_reproduction: float):
        self.max_life_time = max_life_time
        self.p_for_death = p_for_death
        self.p_for_reproduction = p_for_reproduction
