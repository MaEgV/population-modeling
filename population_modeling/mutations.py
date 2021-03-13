from abc import abstractmethod

from scipy.stats import norm  # type: ignore
from math import fabs

from population_modeling.genome import Genome


class MutationalProcesses:
    """
    Base class for different mutational processes. Include variation of maximum lifetime, death probability
    and reproduction probability for the child. Spontaneous mutation happens directly with the individual.

    Methods
    -------

    mutation(self) -> None
        Realize random mutation of the genome's parameters
    child_max_n(self) -> int
        Realize mutation of maximum lifetime
    child_p_for_death(self) -> float
        Realize mutation of death probability
    child_p_for_reproduction(self) -> float
        Realize mutation of reproduction probability
    """
    @abstractmethod
    def _child_max_n(self, parent_genome: Genome):
        raise NotImplementedError

    @abstractmethod
    def _child_p_for_death(self, parent_genome: Genome):
        raise NotImplementedError

    @abstractmethod
    def _child_p_for_reproduction(self, parent_genome: Genome):
        raise NotImplementedError

    @abstractmethod
    def mutation(self, genome: Genome):
        raise NotImplementedError

    def child_genome(self, parent_genome: Genome) -> Genome:
        """

        Creates a descendant genome based on the parent genome

        Returns
        -------
        Genome
            Child's genome
        """

        childs_genome = Genome(
            self._child_max_n(parent_genome),
            self._child_p_for_death(parent_genome),
            self._child_p_for_reproduction(parent_genome)
        )

        return childs_genome


class NormalMutations(MutationalProcesses):
    """
    Include mutational processes based on normal distribution.

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
    PARAMS_SPONTANEOUS_MUTATION = {'loc': 0, 'scale': 0.001}
    PARAMS_MAX_N_VARIATION = {'loc': 0, 'scale': 3}
    PARAMS_CHILD_VARIATION = {'loc': 0, 'scale': 0.01}

    def _child_max_n(self, parent_genome: Genome):
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

        variation = norm.rvs(**NormalMutations.PARAMS_MAX_N_VARIATION)

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

        variation = norm.rvs(**NormalMutations.PARAMS_CHILD_VARIATION)
        parameter = fabs(parent_genome.p_for_death + variation)

        return min(parameter, NormalMutations.MAX_PROBABILITY)

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

        variation = norm.rvs(**NormalMutations.PARAMS_CHILD_VARIATION)
        parameter = fabs(parent_genome.p_for_reproduction + variation)

        return min(parameter, NormalMutations.MAX_PROBABILITY)

    def mutation(self, genome: Genome) -> None:
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

        genome.p_for_death = min(genome.p_for_death + norm.rvs(**NormalMutations.PARAMS_SPONTANEOUS_MUTATION),
                                 NormalMutations.MAX_PROBABILITY)
        genome.p_for_reproduction = min(genome.p_for_reproduction + norm.rvs(**NormalMutations.
                                        PARAMS_SPONTANEOUS_MUTATION), NormalMutations.MAX_PROBABILITY)
