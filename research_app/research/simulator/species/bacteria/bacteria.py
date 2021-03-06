from typing import ClassVar

from research_app.research.simulator import AbstractSelector # type: ignore
from research_app.research.simulator import AbstractMutator # type: ignore
from research_app.research.simulator import AbstractSpecies # type: ignore
from research_app.research.simulator import Genome # type: ignore
from research_app.research.exceptions import DeadBacteriaException
from dataclasses import dataclass, field
from .bacteria_properties import BacteriaProperties


@dataclass
class Bacteria(AbstractSpecies):
    """
    Represents bacteria with its parameters

    Attributes
    ----------
    _properties: BacteriaProperties
    Bacteria status about age and life: die or alive

    _children_max: int
    Maximum number of children in one iteration
    """
    _properties: BacteriaProperties = field(default_factory=BacteriaProperties)
    _children_max: ClassVar[int] = field(init=False, default=2)

    def produce_children(self, selector: AbstractSelector, mutator: AbstractMutator) -> list:
        """
        Life iteration of bacteria

        Parameters
        ----------
        selector: AbstractSelector
            Selection operator
        mutator: AbstractMutator
            Mutation operator

        Returns
        -------
        list
        """
        if not self.is_alive():
            raise DeadBacteriaException(str(self))

        return self._get_children(selector, mutator)

    def evolve(self, selector: AbstractSelector, mutator: AbstractMutator) -> bool:
        """
        One life iteration. An individual change its state within this method

        Parameters
        ----------
        selector: AbstractSelector
            Implementation of the selector that performs the evolution selection

        mutator: AbstractMutator
            Implementation of a mutator that determines genome variability and offspring

        Returns
        -------
            Is alive
        """
        if not self._properties.get_is_alive():
            raise DeadBacteriaException(str(self))

        mutator.mutate(self._genome)

        self._properties.inc_age()

        if self._properties.get_age() > self._genome.max_life_time or selector.is_died(self._genome):
            self._die()

        return self.is_alive()

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

        selector: AbstractSelector
            Make decisions about bacteria's future actions

        Returns
        -------
        Descendants
            Bacteria's children (if they are be)

        """

        children = list() # type: ignore

        while selector.have_to_reproduce(self._genome) and len(children) <= self._children_max:  # the Bernoulli
            # test
            child_genome = mutation_mode.child_genome(self._genome)
            children.append(Bacteria(child_genome))
        return children

    def get_parameters_dict(self) -> Genome:
        genome = self.get_genome_dict()
        genome['age'] = self._properties.get_age()
        return genome

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
