import pytest

from research_app.research.simulator import create_bacteria
from research_app.research.simulator import UniformSelector
from research_app.research.simulator import SelectorParameters
from research_app.research.simulator import NormalMutator


class Case:
    def __init__(self, name, population_max, max_life_time, p_for_death,
                 p_for_reproduction, mutator, selector):
        self.name = name
        self.population_max = population_max
        self.bacteria = create_bacteria(max_life_time, p_for_death, p_for_reproduction)
        self.mutator = mutator
        self.selector = selector


TEST_CASES_BACTERIA_ITERATION = [Case(name="Simple case", population_max=10,
                                      max_life_time=5, p_for_death=0.1, p_for_reproduction=0.1,
                                      mutator=NormalMutator(), selector=UniformSelector(SelectorParameters(0, 1)))]


@pytest.mark.parametrize('bacteria_iteration_alive', TEST_CASES_BACTERIA_ITERATION, ids=str)
def test_iterator_alive(bacteria_iteration_alive: Case) -> None:
    result = bacteria_iteration_alive.bacteria.produce_children(bacteria_iteration_alive.selector,
                                                                bacteria_iteration_alive.mutator)
    assert len(result.get_species()) >= 0


@pytest.mark.parametrize('bacteria_iteration_dead', TEST_CASES_BACTERIA_ITERATION, ids=str)
def test_iterator_dead(bacteria_iteration_dead: Case) -> None:
    bacteria_iteration_dead.bacteria._properties.die()
    with pytest.raises(BaseException):
        bacteria_iteration_dead.bacteria.produce_children(bacteria_iteration_dead.selector,
                                                          bacteria_iteration_dead.mutator)