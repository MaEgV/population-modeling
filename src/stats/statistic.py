from copy import deepcopy
from src.population_modeling.selector.selector import DefaultSelector

from src.population_modeling.population import Population
from src.population_modeling import AbstractSelector, AbstractMutator, NormalMutator, SelectorParams, ExternalFactors
from src.population_modeling.life_cycle import LifeCycle
from pandas import DataFrame
import numpy as np


class PopulationStats:
    """
        Class with some statistical tools for population analysis.

        Attributes
        ----------
        cycle: LifeCycle
            Lifetime cycle of bacteria's population

        Methods
        -------
        num_of_individuals(self, num_iter: int, selector: AbstractSelector, mutator: AbstractMutator,
                           draw_func) -> DataFrame
        Show number of individuals in population
        """

    def __init__(self, bacterias: list):
        self._bacterias = bacterias

    def num_of_individuals(self,
                           num_iter: int,
                           selector: AbstractSelector = DefaultSelector(SelectorParams(0, 0.001),
                                                                        ExternalFactors(0, 0)),
                           mutator: AbstractMutator = NormalMutator()) -> DataFrame:
        """
        Give data in DataFrame about population size and state on each iteration

        Attributes
        ----------
        num_iter: int: Population
            Number of supposed iterations

        selector: AbstractSelector
            Chosen selector for this population

        mutator: AbstractMutator
                Chosen mutator for this population

        Returns
        -------
        DataFrame
            Table with state of population on each iteration

        """
        cycle = LifeCycle(Population(deepcopy(self._bacterias)))
        num_ind = list()
        alive_num = list()
        dead_num = list()
        for num in range(num_iter):
            cycle.iterate(selector, mutator)
            num_ind.append(cycle.population.get_number_individuals())
            alive_num_i, dead_num_i = cycle.population.get_alive_and_dead()
            alive_num.append(alive_num_i)
            dead_num.append(dead_num_i)
        return DataFrame(np.array([[i for i in range(1, num_iter + 1)], num_ind, alive_num, dead_num]).transpose(),
                         columns=['iterations', 'number_of_individuals', 'alive_individuals', 'dead_individuals'])
