from src.population import create_bacteria
from src.research.statistic import Stats, ResearchParams

init_group = [create_bacteria(5, 0.6, 0.2) for i in range(5)]

stats = Stats(init_group)

iteration_params = ResearchParams('uniform', 'default', 'normal', 'default')

# Получить возможные строки(можно пихать эти массивы в выпадающие окошки пока что):
print(ResearchParams.get_modes())

print(stats.research(10, iteration_params).data) # -> фрейм с 10-ю строками, можно сделать не 10, а 1 и на каждой итерации менять params