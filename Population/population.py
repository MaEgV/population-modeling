from Bacteria.bacteria import create_bacteria
from Population.parameters import Parameters
from Population.iterator import Iterator


class Population:
    """
    Attributes
    ----------

    Methods
    -------
    """

    def __init__(self,
                 initial_parameters: Parameters,
                 n: int,
                 max_life_time=5,
                 p_for_death=0.5,
                 p_for_reproduction=0.5):
        self._max_n = n  # max number of iteration. If None - number of iterations is unlimited
        self._first_bacteria = create_bacteria(self, max_life_time, p_for_death, p_for_reproduction)
        self.p = initial_parameters

    def __iter__(self) -> Iterator:
        return Iterator(self._max_n, self._first_bacteria)
