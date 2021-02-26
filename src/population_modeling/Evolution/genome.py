from abc import abstractmethod, ABC
from scipy.stats import norm, uniform
from math import fabs


# class MutationalProcesses:
#     @abstractmethod
#     def child_max_n(self, parent_genome: Genome):
#         raise NotImplementedError
#
#     @abstractmethod
#     def child_p_for_death(self, parent_genome: Genome):
#         raise NotImplementedError
#
#     @abstractmethod
#     def child_p_for_reproduction(self, parent_genome: Genome):
#         raise NotImplementedError
#
#     @abstractmethod
#     def spontaneous_mutation(self, genome: Genome):
#         raise NotImplementedError


# class NormalMutations(MutationalProcesses):
#     def child_max_n(self, parent_genome: Genome) -> int:
#         variation = norm.rvs(0, 3)
#
#         return round(fabs(parent_genome.max_life_time + variation))
#
#     def child_p_for_death(self, parent_genome: Genome) -> float:
#         variation = norm.rvs(0, 0.01)
#         parameter = fabs(parent_genome.p_for_death + variation)
#
#         return min(parameter, 1)
#
#     def child_p_for_reproduction(self, parent_genome: Genome) -> float:
#         variation = norm.rvs(0, 0.01)
#         parameter = fabs(parent_genome.p_for_reproduction + variation)
#
#         return min(parameter, 1)
#
#     def spontaneous_mutation(self, genome: Genome) -> None:
#         genome.p_for_death = min(genome.p_for_death + norm.rvs(0, 0.001), 1)
#         genome.p_for_death = min(genome.p_for_reproduction + norm.rvs(0, 0.001), 1)


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
    """
    def __init__(self, max_life_time_: int, p_for_death_: float, p_for_reproduction_: float):
        self.max_life_time = max_life_time_
        self.p_for_death = p_for_death_
        self.p_for_reproduction = p_for_reproduction_

    def child_genome(self):
        child_genome = Genome(
            self.child_max_n(),
            self.child_p_for_death(),
            self.child_p_for_reproduction()
        )

        return child_genome

    def spontaneous_mutation(self) -> None:
        self.p_for_death = min(self.p_for_death + norm.rvs(0, 0.001), 1)
        self.p_for_reproduction = min(self.p_for_reproduction + norm.rvs(0, 0.001), 1)

    def child_max_n(self) -> int:
        variation = norm.rvs(0, 3)

        return round(fabs(self.max_life_time + variation))

    def child_p_for_death(self) -> float:
        variation = norm.rvs(0, 0.01)
        parameter = fabs(self.p_for_death + variation)

        return min(parameter, 1)

    def child_p_for_reproduction(self) -> float:
        variation = norm.rvs(0, 0.01)
        parameter = fabs(self.p_for_reproduction + variation)

        return min(parameter, 1)

