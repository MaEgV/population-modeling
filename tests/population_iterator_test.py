import pytest
from population_modeling import create_bacteria
from population_modeling.population import create_population
from population_modeling.mutations.normal_mutation import NormalMutations
from population_modeling.population_iteration import iterate
from population_modeling.selector import Selector, ExternalFactors
from population_modeling.mutations.variation_parameters import MutationalParams


class Case:
    def __init__(self, name,  max_life_time, antagonism, overpopulation, p_for_death,
                 p_for_reproduction, result, mutation_mode):
        self.name = name
        self.bacteria = create_bacteria(max_life_time, p_for_death, p_for_reproduction)
        self.population = create_population(self.bacteria)
        self.result = result
        self.mutation_mode = mutation_mode
        self.selector = Selector(ExternalFactors(antagonism, overpopulation))


TEST_CASES_POPULATION_ITERATOR_ZERO = [Case(name="Zero iterations", antagonism=0, overpopulation=0, max_life_time=0,
                                            p_for_death=1, p_for_reproduction=0, result=1,
                                            mutation_mode=NormalMutations(MutationalParams(0, 0.001),
                                                                          MutationalParams(0, 3),
                                                                          MutationalParams(0, 0.01)))]

TEST_CASES_POPULATION_ITERATOR = [Case(name="One offspring", antagonism=0, overpopulation=0, max_life_time=5,
                                       p_for_death=0.3, p_for_reproduction=0.7, result=1,
                                       mutation_mode=NormalMutations(MutationalParams(0, 0.001),
                                                                     MutationalParams(0, 3),
                                                                     MutationalParams(0, 0.01)))]


@pytest.mark.parametrize('population_iterator', TEST_CASES_POPULATION_ITERATOR_ZERO, ids=str)
def test_iterator_population_one(population_iterator: Case) -> None:
    result = iterate(population_iterator.population, population_iterator.selector, population_iterator.mutation_mode)
    graph = result.genealogical_tree
    assert graph.vcount() == population_iterator.result


@pytest.mark.parametrize('population_iterator', TEST_CASES_POPULATION_ITERATOR, ids=str)
def test_iterator_population(population_iterator: Case) -> None:
    result = iterate(population_iterator.population, population_iterator.selector, population_iterator.mutation_mode)
    graph = result.genealogical_tree
    assert graph.vcount() >= population_iterator.result
