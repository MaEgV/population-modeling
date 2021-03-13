import pytest
from population_modeling import bacteria, ExternalFactors
from population_modeling.bacteria_iteration import iterate
from population_modeling.mutations import NormalMutations
from population_modeling.selector import Selector


class Case:
    def __init__(self, name, population_max, antagonism, overpopulation, max_life_time, p_for_death,
                 p_for_reproduction, mutation_mode):
        self.name = name
        self.population_max = population_max
        self.antagonism = antagonism
        self.overpopulation = overpopulation
        self.bacteria = bacteria.create_bacteria(max_life_time, p_for_death, p_for_reproduction)
        self.mutation_mode = mutation_mode


TEST_CASES_BACTERIA_ITERATION = [Case(name="Simple case", population_max=10, antagonism=0, overpopulation=0,
                                      max_life_time=5, p_for_death=0.1, p_for_reproduction=0.1,
                                      mutation_mode=NormalMutations())]


@pytest.mark.parametrize('bacteria_iteration_alive', TEST_CASES_BACTERIA_ITERATION, ids=str)
def test_iterator_alive(bacteria_iteration_alive: Case) -> None:
    result = iterate(Selector(
        ExternalFactors(bacteria_iteration_alive.antagonism, bacteria_iteration_alive.overpopulation)),
        bacteria_iteration_alive.mutation_mode, bacteria_iteration_alive.bacteria)
    assert len(result) >= 0


@pytest.mark.parametrize('bacteria_iteration_dead', TEST_CASES_BACTERIA_ITERATION, ids=str)
def test_iterator_dead(bacteria_iteration_dead: Case) -> None:
    bacteria_iteration_dead.bacteria.is_alive = False
    with pytest.raises(BaseException):
        iterate(Selector(ExternalFactors(bacteria_iteration_dead.antagonism, bacteria_iteration_dead.overpopulation)),
                bacteria_iteration_dead.mutation_mode, bacteria_iteration_dead.bacteria)
