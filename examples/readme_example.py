from population_modeling import Population, Selector, ExternalFactors

param = Selector(ExternalFactors())  # creating the initial parameters of the population and selector
population = Population(param, p_for_death=0.1, p_for_reproduction=0.5, max_life_time=10) # creating population

for _ in range(10):
    population.iteration().draw()  # drawing a population without saving