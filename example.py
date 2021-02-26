from src.population_modeling.Population.population import Population
from src.population_modeling.Population.parameters import Parameters

param = Parameters(0, 0)
c = 0
t = Population(param, p_for_death=0.1, p_for_reproduction=0.5, max_life_time=10)

for i in range(10):
    t.iteration().draw()

