from src.population_modeling import Population, Selector, ExternalFactors

param = Selector(ExternalFactors())
population = Population(param, p_for_death=0.1, p_for_reproduction=0.5, max_life_time=10)

for _ in range(10):
    population.iteration().draw()
