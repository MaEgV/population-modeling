from abc import abstractmethod

from scipy.stats import norm  # type: ignore
from math import fabs


class Genome:
    """

    Class for description of bacteria's genome.

    Attributes
    ----------
    max_life_time : int
        Maximum iterations for bacteria

    p_for_death : float
        Probability of death

    p_for_reproduction : float
        Probability of reproduction

    Methods
    -------
    child_genome(self) -> Genome
        Returns generated child's genome

    """

    def __init__(self, max_life_time_: int, p_for_death_: float, p_for_reproduction_: float):
        self.max_life_time = max_life_time_
        self.p_for_death = p_for_death_
        self.p_for_reproduction = p_for_reproduction_
        self.mutation_type = NormalMutations()

    def child_genome(self):
        """

        Creates a descendant genome based on the parent genome

        Returns
        -------
        Genome
            Child's genome
        """

        child_genome = Genome(
            self.mutation_type.child_max_n(self),
            self.mutation_type.child_p_for_death(self),
            self.mutation_type.child_p_for_reproduction(self)
        )

        return child_genome


class MutationalProcesses:
    """
    Base class for different mutational processes. Include variation of maximum lifetime, death probability
    and reproduction probability for the child. Spontaneous mutation happens directly with the individual.

    Methods
    -------

    spontaneous_mutation(self) -> None
        Realize random mutation of the genome's parameters
    child_max_n(self) -> int
        Realize mutation of maximum lifetime
    child_p_for_death(self) -> float
        Realize mutation of death probability
    child_p_for_reproduction(self) -> float
        Realize mutation of reproduction probability
    """
    @abstractmethod
    def child_max_n(self, parent_genome: Genome):
        raise NotImplementedError

    @abstractmethod
    def child_p_for_death(self, parent_genome: Genome):
        raise NotImplementedError

    @abstractmethod
    def child_p_for_reproduction(self, parent_genome: Genome):
        raise NotImplementedError

    @abstractmethod
    def spontaneous_mutation(self, genome: Genome):
        raise NotImplementedError


class NormalMutations(MutationalProcesses):
    """
    Include mutational processes based on normal distribution.

    Methods
    -------
    def child_genome(self) -> Genome
        Returns generated child's genome
    spontaneous_mutation(self) -> None
        Realize random mutation of the genome's parameters
    child_max_n(self) -> int
        Realize mutation of maximum lifetime
    child_p_for_death(self) -> float
        Realize mutation of death probability
    child_p_for_reproduction(self) -> float
        Realize mutation of reproduction probability
    """

    MAX_PROBABILITY = 1
    PARAMS_SPONTANEOUS_MUTATION = [0, 0.001]
    PARAMS_MAX_N_VARIATION = [0, 3]
    PARAMS_PROBABILITY_VARIATION = [0, 0.01]

    def child_max_n(self, parent_genome: Genome):
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

        variation = norm.rvs(*NormalMutations.PARAMS_MAX_N_VARIATION)

        return round(fabs(parent_genome.max_life_time + variation))

    def child_p_for_death(self, parent_genome: Genome) -> float:
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

        variation = norm.rvs(*NormalMutations.PARAMS_PROBABILITY_VARIATION)
        parameter = fabs(parent_genome.p_for_death + variation)

        return min(parameter, NormalMutations.MAX_PROBABILITY)

    def child_p_for_reproduction(self, parent_genome: Genome) -> float:
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

        variation = norm.rvs(*NormalMutations.PARAMS_PROBABILITY_VARIATION)
        parameter = fabs(parent_genome.p_for_reproduction + variation)

        return min(parameter, NormalMutations.MAX_PROBABILITY)

    def spontaneous_mutation(self, genome: Genome) -> None:
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

        genome.p_for_death = min(genome.p_for_death + norm.rvs(*NormalMutations.PARAMS_SPONTANEOUS_MUTATION),
                                 NormalMutations.MAX_PROBABILITY)
        genome.p_for_reproduction = min(genome.p_for_reproduction + norm.rvs(*NormalMutations.
                                        PARAMS_SPONTANEOUS_MUTATION), NormalMutations.MAX_PROBABILITY)
