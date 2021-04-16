from .abstract_selector import AbstractSelector, SelectorParams
from ..genome import Genome
from scipy.stats import uniform  # type: ignore


class ExternalFactors:
    """

    A class of population parameters that allows you to learn about the state of the population.

    With the help of this class of bacteria are able to control their size and composition.
    Play the role of external factors of evolution.

    Attributes
    ----------
    antagonism : float
        External factor which increases death probability

    overpopulation : float
        Degree of overcrowding. Influence on reproduction probability.

    """

    def __init__(self, antagonism: float = 0, overpopulation: float = 0):
        self.antagonism = antagonism  # may be negative (collaboration)
        self.overpopulation = overpopulation


class UniformSelector(AbstractSelector):
    def __init__(self,
                 params: SelectorParams):
        self.params = params

    def is_died(self, genome: Genome) -> bool:
        """

        Decide if bacteria should die or not based on lifetime

        Parameters
        ----------
        genome: Genome
            Bacteria's genome

        Returns
        -------
        bool
            Decision: dead (true) or alive (false)
        """
        return genome.p_for_death > uniform.rvs(self.params.loc, self.params.scale)

    def have_to_reproduct(self, genome: Genome) -> bool:
        """

        Decide if bacteria should reproduct or not

        Parameters
        ----------
        genome: Genome
            Bacteria's genome

        Returns
        -------
        bool
            Decision: should reproduct (true) or shouldn't (false)
        """
        return genome.p_for_reproduction > uniform.rvs(self.params.loc, self.params.scale)
