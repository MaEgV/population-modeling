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

           Methods
       -------
        is_alive(self) -> bool
            Returns status of life status: alive or die

        inc_age(self) -> None
            Increment age counter

        die(self) -> None
            Kill the bacteria

    """

    is_alive: bool = field(init=False, default=True)
    age: int = field(init=False, default=0)

    def get_is_alive(self) -> bool:
        """
        True if bacteria is alive, else - False

        Returns
        -------
        bool
            Bacteria status
        """

        return self.is_alive

    def inc_age(self, max_life_time: int) -> None:

        """
        Increase age counter of bacteria
        When the age exceeds the max_life_time from the genome, the bacteria automatically dies

        Parameters
        ----------
        max_life_time: int
            Maximum bacteria's lifetime

        Returns
        -------
        None
        """

        self.age += 1

        if self.age > max_life_time:
            self.is_alive = False

    def die(self) -> None:
        """
        Changes the status to deceased

        Returns
        -------
        None
        """

        self.is_alive = False


@dataclass(frozen=True)
class Bacteria:
    """
       Represents bacteria with its parameters

       Attributes
       ----------
       _status: BacteriaStatus
           Bacteria status about age and life: die or alive

       genome : Genome
           Genome of bacteria

       """

    genome: Genome
    status: BacteriaStatus = field(default_factory=BacteriaStatus)


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
