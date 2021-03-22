from dataclasses import dataclass


@dataclass()
class Genome:
    """
    Dataclass for inherited parameters of bacteria

    Attributes
    ----------
    max_life_time : int
        Maximum iterations for bacteria

    p_for_death : float
        Probability of death

    p_for_reproduction : float
        Probability of reproduction

    """
    max_life_time: int
    p_for_death: float
    p_for_reproduction: float
