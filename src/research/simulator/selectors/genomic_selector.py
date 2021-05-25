from .abstract_selector import AbstractSelector, SelectorParameters
from src.research.simulator.genome import Genome
from scipy.stats import uniform  # type: ignore


class UniformSelector(AbstractSelector):
    def __init__(self,
                 params: SelectorParameters):
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
        return genome.p_for_death < uniform.rvs(self.params.loc, self.params.scale)

    def have_to_reproduce(self, genome: Genome) -> bool:
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
