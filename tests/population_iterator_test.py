import pytest

from src.population_research.researcher.population_research import Population
from src.population_research.simulator import create_bacteria
from src.population_research.simulator.selectors.genomic_selector import UniformSelector, SelectorParameters

from src.population_research.simulator.mutations.normal_mutator import NormalMutator


class Case:
    def __init__(self, name, result, selector, mutator, p_for_reproduction):
        self.name = name
        self.bacteria = create_bacteria(p_for_reproduction=p_for_reproduction)
        self.result = result
        self.mutator = mutator
        self.selector = selector
        self.population = Population()
        self.population.add_generation([self.bacteria])


TEST_CASES_POPULATION_ITERATOR_ZERO = [Case(name="Zero iterations", result=1,
                                            mutator=NormalMutator(),
                                            selector=UniformSelector(SelectorParameters(0, 1)), p_for_reproduction=0)
                                       ]

TEST_CASES_POPULATION_ITERATOR = [Case(name="One offspring", result=1,
                                       mutator=NormalMutator(),
                                       selector=UniformSelector(SelectorParameters(0, 1)), p_for_reproduction=0.8)]


@pytest.mark.parametrize('population_iterator', TEST_CASES_POPULATION_ITERATOR_ZERO, ids=str)
def test_iterator_population_one(population_iterator: Case) -> None:
    population_iterator.population.produce_new_generation(population_iterator.selector,
                                                          population_iterator.mutator)

    all_individuals = len(population_iterator.population.get_individuals())
    assert all_individuals == population_iterator.result

@pytest.mark.parametrize('population_iterator', TEST_CASES_POPULATION_ITERATOR, ids=str)
def test_iterator_population(population_iterator: Case) -> None:
    population_iterator.population.produce_new_generation(population_iterator.selector,
                                                          population_iterator.mutator)

    all_individuals = len(population_iterator.population.get_individuals())
    assert all_individuals >= population_iterator.result
