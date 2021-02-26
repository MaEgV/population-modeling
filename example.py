from src.population_modeling.Population.parameters import Parameters
from src.population_modeling.Population.population import Population

param = Parameters(0, 0)
for i in Population(param, n=15, p_for_death=0.2, p_for_reproduction=0.4, max_life_time=10):
    i.draw()
