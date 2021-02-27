import pytest
from src.population_modeling.Bacteria.bacteria import create_bacteria
from src.population_modeling.Population.population import Parameters, Population


class Case:
    def __init__(self, name, population_max, antagonism, overpopulation, max_life_time, p_for_death,
                 p_for_reproduction):
        self.name = name
        self.population_max = population_max
        self.antagonism = antagonism
        self.overpopulation = overpopulation
        self.bacteria = create_bacteria(max_life_time, p_for_death, p_for_reproduction)


TEST_CASES_BACTERIA_ITERATION = [Case(name="Simple case", population_max=10, antagonism=0, overpopulation=0,
                                      max_life_time=5, p_for_death=0.1, p_for_reproduction=0.1)]


@pytest.mark.parametrize('bacteria_iteration_alive', TEST_CASES_BACTERIA_ITERATION, ids=str)
def test_iterator_alive(bacteria_iteration_alive: Case) -> None:
    result = bacteria_iteration_alive.bacteria.iteration(Parameters(bacteria_iteration_alive.population_max,
                                                                    bacteria_iteration_alive.antagonism,
                                                                    bacteria_iteration_alive.overpopulation))
    assert len(result) >= 0


@pytest.mark.parametrize('bacteria_iteration_dead', TEST_CASES_BACTERIA_ITERATION, ids=str)
def test_iterator_dead(bacteria_iteration_dead: Case) -> None:
    bacteria_iteration_dead.bacteria.is_alive = False
    with pytest.raises(BaseException):
        bacteria_iteration_dead.bacteria.iteration(Parameters(bacteria_iteration_dead.population_max,
                                                              bacteria_iteration_dead.antagonism,
                                                              bacteria_iteration_dead.overpopulation))
