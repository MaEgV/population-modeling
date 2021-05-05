from src.population import create_bacteria
from src.research.population_research import Research, IterationParameters


research = Research()
research.add_individual([create_bacteria(5, 0, 0.2) for _ in range(10)])

print(research)

iteration_params = IterationParameters('uniform', 1, 'normal', 0.0001)  # тут scale для мутатора и селектора и их тип

# Получить возможные строки(можно пихать эти массивы в выпадающие окошки пока что):
print(IterationParameters.get_modes())

print(research.build(4, iteration_params).data) # -> фрейм с 10-ю строками, можно сделать не 10, а 1 и на каждой итерации менять params
print(research.build(4, iteration_params).data) # -> фрейм с 10-ю строками, можно сделать не 10, а 1 и на каждой итерации менять params