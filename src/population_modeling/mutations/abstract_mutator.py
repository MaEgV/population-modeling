from abc import abstractmethod
from src.population_modeling.genome import Genome


class AbstractMutator:
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
    def _child_max_n(self, parent_genome: Genome) -> int:
        raise NotImplementedError

    @abstractmethod
    def _child_p_for_death(self, parent_genome: Genome) -> float:
        raise NotImplementedError

    @abstractmethod
    def _child_p_for_reproduction(self, parent_genome: Genome) -> float:
        raise NotImplementedError

    @abstractmethod
    def mutate(self, genome: Genome) -> None:
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

