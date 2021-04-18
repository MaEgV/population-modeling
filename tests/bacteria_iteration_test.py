import pytest
from src.population import ExternalFactors, UniformSelector
from src.population.individuals import bacteria
from src.population.mutations.normal_mutator import NormalMutator
from src.population.life_cycle import bacteria_cycle
from src.population.mutations.mutator_parameters import MutatorParams
from src.population.selectors.selector_params import SelectorParams

class Case:
    def __init__(self, name, population_max, antagonism, overpopulation, max_life_time, p_for_death,
                 p_for_reproduction, mutation_mode, ):
        self.name = name
        self.population_max = population_max
        self.antagonism = antagonism
        self.overpopulation = overpopulation
        self.bacteria = bacteria.create_bacteria(max_life_time, p_for_death, p_for_reproduction)
        self.mutation_mode = mutation_mode


TEST_CASES_BACTERIA_ITERATION = [Case(name="Simple case", population_max=10, antagonism=0, overpopulation=0,
                                      max_life_time=5, p_for_death=0.1, p_for_reproduction=0.1,
                                      mutation_mode=NormalMutator(MutatorParams(0, 0.001),
                                                                  MutatorParams(0, 3),
                                                                  MutatorParams(0, 0.01)))]


@pytest.mark.parametrize('bacteria_iteration_alive', TEST_CASES_BACTERIA_ITERATION, ids=str)
def test_iterator_alive(bacteria_iteration_alive: Case) -> None:
    result = bacteria_cycle(bacteria_iteration_alive.bacteria, UniformSelector(
        SelectorParams(0, 1),
        ExternalFactors(bacteria_iteration_alive.antagonism, bacteria_iteration_alive.overpopulation)),
                            bacteria_iteration_alive.mutation_mode)
    assert len(result) >= 0


@pytest.mark.parametrize('bacteria_iteration_dead', TEST_CASES_BACTERIA_ITERATION, ids=str)
def test_iterator_dead(bacteria_iteration_dead: Case) -> None:
    bacteria_iteration_dead.bacteria._properties.die()
    with pytest.raises(BaseException):
        bacteria_cycle(bacteria_iteration_dead.bacteria, UniformSelector(
            SelectorParams(0, 1),
            ExternalFactors(bacteria_iteration_dead.antagonism, bacteria_iteration_dead.overpopulation)),
                       bacteria_iteration_dead.mutation_mode)
