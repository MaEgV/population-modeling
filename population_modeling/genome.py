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

    Methods
    -------

    update(self, **kwargs) -> None
        Update genome parameters, which indicated in parameter 'params'

    """
    max_life_time: int
    p_for_death: float
    p_for_reproduction: float

    def update(self, **params) -> None:
        """

        Update genome parameters, which indicated in parameter 'params'

        Parameters
        ----------
        params: dict(float)
            Dictionary with parameters

        Returns
        -------
        None

        """
        self.p_for_death = params['p_for_death']
        self.p_for_reproduction = params['p_for_reproduction']
