import pytest

from src.population_research.population.populations import Population
from src.population_research.research.population_research import Research, IterationParameters
from src.population_research.research.parameters import IndividualParameters


class Case:
    def __init__(self, name, selector: str, selector_mode: float, mutator: str, mutator_mode: float, result):
        self.name = name
        self.research = Research(Population())
        self.research.add_individual(IndividualParameters('bacteria', 10, 0.4, 0.6))
        self.result = result
        self.iter_params = IterationParameters(selector, selector_mode, mutator, mutator_mode)


TEST_CASES_RESEARCH = [Case(name="Research", result=1, mutator_mode=1,
                            selector_mode=0.001, selector='uniform',
                            mutator='normal')]


@pytest.mark.parametrize('research_obj', TEST_CASES_RESEARCH, ids=str)
def test_iterator_population_one(research_obj: Case) -> None:
    research_result = research_obj.research.build(2, research_obj.iter_params)
    assert len(research_result.data['alive']) == 2
