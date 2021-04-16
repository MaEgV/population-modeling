from typing import List

from src.population.selectors.abstract_selector import AbstractSelector
from src.population.exceptions import DeadBacteriaException
from src.population.individuals.abstract_individual import AbstractIndividual
from src.population import Genome, AbstractMutator
from dataclasses import dataclass, field


@dataclass
class BacteriaProperties:
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
    get_is_alive(self) -> bool
        Returns status of life status: alive or die

    inc_age(self) -> None
         Increment age counter

    get_age(self) -> int:
        Returns age

    die(self) -> None
        Kill the bacteria

    """
    _is_alive: bool = field(init=False, default=True)
    _age: int = field(init=False, default=0)

    def get_is_alive(self) -> bool:
        """
        True if bacteria is alive, else - False

        Returns
        -------
        bool
            Bacteria status
        """

        return self._is_alive

    def inc_age(self) -> None:

        """
        Increase age counter of bacteria
        When the age exceeds the max_life_time from the genome, the bacteria automatically dies

        Returns
        -------
        None
        """

        self._age += 1

    def get_age(self) -> int:
        """
        Getter of the age property

        Returns
        -------
        int
            age property
        """
        return self._age

    def die(self) -> None:
        """
        Changes the status to deceased

        Returns
        -------
        None
        """

        self._is_alive = False


@dataclass(frozen=True)
class Bacteria(AbstractIndividual):
    """
       Represents bacteria with its parameters

       Attributes
       ----------
       _properties: BacteriaProperties
           Bacteria status about age and life: die or alive
       """

    _properties: BacteriaProperties = field(default_factory=BacteriaProperties)

    def cycle(self, selector: AbstractSelector, mutator: AbstractMutator) -> List[AbstractIndividual]:
        """
        Life iteration of bacteria

        Parameters
        ----------
        bacteria: Bacteria
            Individual bacteria, witch is iterated
        selector: AbstractSelector
            Selection operator
        mutator: AbstractMutator
            Mutation operator

        Returns
        -------
        list
        """
        if not self._properties.get_is_alive():
            raise DeadBacteriaException(str(self))

        mutator.mutate(self._genome)

        self._properties.inc_age()

        if selector.is_died(self._genome):
            self._die()
            return []

        return self._get_children(selector, mutator)

    def is_alive(self) -> bool:
        """
        True if bacteria is alive, else - False

        Returns
        -------
        bool
            Bacteria status
        """

        return self._properties.get_is_alive()

    def _die(self) -> None:
        """
        Changes live status to false

        Returns
        -------
        None
        """

        if not self.is_alive():
            raise DeadBacteriaException(str(self))

        self._properties.die()

    def _get_children(self, selector: AbstractSelector, mutation_mode: AbstractMutator) -> list:
        """
        Generate bacteria's children

        Parameters
        ----------
        mutation_mode: AbstractMutator
            Implementation of mutation mechanisms

        bacteria: Bacteria
            A bacterium whose descendants may appear

        selector: AbstractSelector
            Make decisions about bacteria's future actions

        Returns
        -------
        list[Bacteria]
            Bacteria's children (if they are be)

        """

        children = list()
        while selector.have_to_reproduct(self._genome):  # the Bernoulli test
            child_genome = mutation_mode.child_genome(self._genome)
            children.append(Bacteria(child_genome))

        return children


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
