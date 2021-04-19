from src.population import create_bacteria
from src.research.statistic import PopulationResearch, ResearchParams


research = PopulationResearch()
research.add_individuals([create_bacteria(5, 0, 0.2) for _ in range(10)])

print(research)

iteration_params = ResearchParams('uniform', 1, 'normal', 0.0001)  # тут scale для мутатора и селектора и их тип

# Получить возможные строки(можно пихать эти массивы в выпадающие окошки пока что):
print(ResearchParams.get_modes())

print(research.research(4, iteration_params).data) # -> фрейм с 10-ю строками, можно сделать не 10, а 1 и на каждой итерации менять params
print(research.research(4, iteration_params).data) # -> фрейм с 10-ю строками, можно сделать не 10, а 1 и на каждой итерации менять params