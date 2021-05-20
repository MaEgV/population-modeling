from scipy.stats import norm  # type: ignore
from math import fabs

from src.population_research.simulator.genome import Genome
from ..mutations.abstract_mutator import AbstractMutator
from ..mutations.mutator_parameters import MutatorParams


class NormalMutator(AbstractMutator):
    """

    Include mutational processes based on normal distribution.

    Attributes
    ----------

    mutational_params: MutatorParams
        Mean and standard deviation for normal mutation

    max_n_params: MutatorParams
        Mean and standard deviation for maximum lifetime variation

    child_params: MutatorParams
            Mean and standard deviation for child's genome variation

    Methods
    -------
    def child_genome(self) -> Genome
        Returns generated child's genome

    mutation(self) -> None
        Realize random mutation of the genome's parameters

    child_max_n(self) -> int
        Realize mutation of maximum lifetime

    child_p_for_death(self) -> float
        Realize mutation of death probability

    child_p_for_reproduction(self) -> float
        Realize mutation of reproduction probability

    """

    MAX_PROBABILITY = 1

    def __init__(self,
                 mutational_params: MutatorParams = MutatorParams(0, 0.01),
                 max_n_params: MutatorParams = MutatorParams(0, 3),
                 child_params: MutatorParams = MutatorParams(0, 0.05)):
        self.mutational_params = mutational_params
        self.max_n_params = max_n_params
        self.child_params = child_params

    def _child_max_n(self, parent_genome: Genome) -> int:
        """

        Generate mutation of maximum lifetime

        Parameters
        ----------
        parent_genome: Genome
            Parent's genome

        Returns
        -------
        int
            New value of maximum lifetime

        """

        variation = norm.rvs(self.max_n_params.loc, self.max_n_params.scale)

        return round(fabs(parent_genome.max_life_time + variation))

    def _child_p_for_death(self, parent_genome: Genome) -> float:
        """

        Generate mutation of death probability

        Parameters
        ----------
        parent_genome: Genome
            Parent's genome

        Returns
        -------
        float
            New value of death probability

        """

        variation = norm.rvs(self.child_params.loc, self.child_params.scale)
        parameter = fabs(parent_genome.p_for_death + variation)

        return min(parameter, NormalMutator.MAX_PROBABILITY)

    def _child_p_for_reproduction(self, parent_genome: Genome) -> float:
        """

        Generate mutation of reproduction probability

        Parameters
        ----------
        parent_genome: Genome
            Parent's genome

        Returns
        -------
        float
            New value of death reproduction

        """

        variation = norm.rvs(self.child_params.loc, self.child_params.scale)
        parameter = fabs(parent_genome.p_for_reproduction + variation)

        return min(parameter, NormalMutator.MAX_PROBABILITY)

    def mutate(self, genome: Genome) -> None:
        """

        Realize spontaneous mutation of the genome

        Parameters
        ----------
        genome
            Bacteria's genome

        Returns
        -------
        None

        """

        new_p_for_death = min(genome.p_for_death + norm.rvs(self.mutational_params.loc, self.mutational_params.scale)
                              , NormalMutator.MAX_PROBABILITY)
        new_p_for_reproduction = min(genome.p_for_reproduction + norm.rvs(self.mutational_params.loc,
                                                                          self.mutational_params.scale),
                                     NormalMutator.MAX_PROBABILITY)
        genome.update(p_for_death=new_p_for_death, p_for_reproduction=new_p_for_reproduction)