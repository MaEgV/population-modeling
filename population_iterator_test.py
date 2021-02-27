import pytest
from src.population_modeling.bacteria import create_bacteria
from src.population_modeling.population import Population, Selector, ExternalFactors

class Case:
    def __init__(self, name, population_max, antagonism, overpopulation, max_life_time, p_for_death,
                 p_for_reproduction, result):
        self.name = name
        self.population = Population(
            Selector(ExternalFactors(antagonism, overpopulation)),
            max_life_time, p_for_death, p_for_reproduction)
        self.max_population = population_max
        self.bacteria = create_bacteria(max_life_time, p_for_death, p_for_reproduction)
        self.result = result


TEST_CASES_POPULATION_ITERATOR_ONE = [Case(name="Zero iterations", population_max=0, antagonism=0, overpopulation=0,
                                           max_life_time=0, p_for_death=1, p_for_reproduction=0, result=1)]


TEST_CASES_POPULATION_ITERATOR = [Case(name="One offspring", population_max=10, antagonism=0, overpopulation=0,
                                       max_life_time=5, p_for_death=0.3, p_for_reproduction=0.7, result=1)]



@pytest.mark.parametrize('population_iterator', TEST_CASES_POPULATION_ITERATOR_ONE, ids=str)
def test_iterator_population_one(population_iterator: Case) -> None:
    result = population_iterator.population.iteration()
    graph = result.graph
    assert graph.vcount() == population_iterator.result


@pytest.mark.parametrize('population_iterator', TEST_CASES_POPULATION_ITERATOR, ids=str)
def test_iterator_population(population_iterator: Case) -> None:
    result = population_iterator.population.iteration()
    graph = result.graph
    assert graph.vcount() >= population_iterator.result

