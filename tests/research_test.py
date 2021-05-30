import pytest

from research_app.research.simulator.populations.population import Population
from research_app.research.research.population_research import Research, ResearchParameters
from research_app.research.research.parameters import IndividualParameters
from research_app.research.simulator.species.bacteria import create_bacteria


class Case:
    def __init__(self, name, selector: str, selector_mode: float, mutator: str, mutator_mode: float, result):
        self.name = name
        self.research = Research()
        self.bacteria = create_bacteria(max_life_time=10, p_for_death=0.4, p_for_reproduction=0.6)
        self.result = result
        self.iter_params = ResearchParameters(selector, selector_mode, mutator, mutator_mode, 2)
        self.population = Population()
        self.population.add_individuals([self.bacteria])


TEST_CASES_RESEARCH = [Case(name="Research", result=1, mutator_mode=1,
                            selector_mode=0.001, selector='uniform',
                            mutator='normal')]


@pytest.mark.parametrize('research_obj', TEST_CASES_RESEARCH, ids=str)
def test_iterator_population_one(research_obj: Case) -> None:
    research_result = research_obj.research.run(research_obj.population, research_obj.iter_params)
    assert len(research_result.data['alive']) == 2
