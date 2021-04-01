import pytest

from population_modeling import create_bacteria
from population_modeling.life_cycle import LifeCycle
from population_modeling.mutations.normal_mutator import NormalMutator
from population_modeling.mutations.variation_parameters import MutationParams
from population_modeling.population import create_population
from population_modeling.selector.selector import DefaultSelector, ExternalFactors
from population_modeling.selector.selector_params import SelectorParams

class Case:
    def __init__(self, name,  max_life_time, antagonism, overpopulation, p_for_death,
                 p_for_reproduction, result, mutation_mode):
        self.name = name
        self.bacteria = create_bacteria(max_life_time, p_for_death, p_for_reproduction)
        self.population = create_population(self.bacteria)
        self.result = result
        self.mutation_mode = mutation_mode
        self.selector = DefaultSelector(SelectorParams(0, 1), ExternalFactors(antagonism, overpopulation))


TEST_CASES_POPULATION_ITERATOR_ZERO = [Case(name="Zero iterations", antagonism=0, overpopulation=0, max_life_time=0,
                                            p_for_death=1, p_for_reproduction=0, result=1,
                                            mutation_mode=NormalMutator(MutationParams(0, 0.001),
                                                                        MutationParams(0, 3),
                                                                        MutationParams(0, 0.01)))]

TEST_CASES_POPULATION_ITERATOR = [Case(name="One offspring", antagonism=0, overpopulation=0, max_life_time=5,
                                       p_for_death=0.3, p_for_reproduction=0.7, result=1,
                                       mutation_mode=NormalMutator(MutationParams(0, 0.001),
                                                                   MutationParams(0, 3),
                                                                   MutationParams(0, 0.01)))]


@pytest.mark.parametrize('population_iterator', TEST_CASES_POPULATION_ITERATOR_ZERO, ids=str)
def test_iterator_population_one(population_iterator: Case) -> None:
    LifeCycle(population_iterator.population).iterate(population_iterator.selector,
                                                      population_iterator.mutation_mode)

    graph = population_iterator.population.genealogical_tree
    assert graph.number_of_nodes() == population_iterator.result


@pytest.mark.parametrize('population_iterator', TEST_CASES_POPULATION_ITERATOR, ids=str)
def test_iterator_population(population_iterator: Case) -> None:
    LifeCycle(population_iterator.population).iterate(population_iterator.selector, population_iterator.mutation_mode)
    graph = population_iterator.population.genealogical_tree
    assert graph.number_of_nodes() >= population_iterator.result
