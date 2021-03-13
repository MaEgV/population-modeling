from population_modeling import *

first_bacteria = create_bacteria(p_for_death=0.1)
population = create_population(first_bacteria)  # creating population

selector = Selector(ExternalFactors())  # creating the initial parameters of the population and selector
mutation_mode = NormalMutations()

for _ in range(10):
    draw(iterate(population, selector, mutation_mode))  # drawing a population without saving