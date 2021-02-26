from Bacteria.bacteria import create_bacteria
from Population.parameters import Parameters
from Population.iterator import Iterator


class Population:
    """
    A class containing information about the population. An iterator is implemented using a class Population.Iterator.
    Bacteria can get information about their population to adjust their behavior

    Attributes
    ----------
    initial_parameters: Parameters
        started parameters of population
    n: int
        max iteration times of population
    max_life_time: int
        max life time of first bacteria
    p_for_death: float
        probability for death per iteration of first bacteria
    p_for_reproduction: float
        probability for reproduce 1 child per iteration of first bacteria (could be many children)

    Methods
    -------
    __iter__(self) -> Iterator:
        get iterator of Population
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
