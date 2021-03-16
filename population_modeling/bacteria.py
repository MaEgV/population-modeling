from population_modeling.selector import Genome
from dataclasses import dataclass, field


@dataclass
class BacteriaStatus:
    """
    A class containing properties of a bacterium that are not inherited by its children.

    Attributes
    ----------
    is_alive : bool
       Is bacteria alive or dead
    age : int
        Current age of bacteria
    """

    is_alive: bool = field(init=False, default=True)
    age: int = field(init=False, default=0)


@dataclass(frozen=True)
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
        is_alive(self) -> bool
            Returns status of aliving
        inc_age(self) -> None
            Increment age counter
        die(self) -> None
            Kill the bacteria
       """

    genome: Genome
    _status: BacteriaStatus = field(default_factory=BacteriaStatus)

    def is_alive(self) -> bool:
        """
        True if bacteria is alive, else - False

        Returns
        -------
        bool
            Bacteria status
        """

        return self._status.is_alive

    def inc_age(self) -> None:
        """
        Increase age counter of bacteria
        When the age exceeds the max_life_time from the genome, the bacteria automatically dies

        Returns
        -------
        None
        """

        self._status.age += 1

        if self._status.age > self.genome.max_life_time:
            self._status.is_alive = False

    def die(self) -> None:
        """
        Changes the status to deceased

        Returns
        -------
        None
        """

        self._status.is_alive = False


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
