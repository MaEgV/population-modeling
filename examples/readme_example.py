from population_modeling import *

first_bacteria = create_bacteria(p_for_death=0.1)  # creating first bacteria to start a population
population = create_population(first_bacteria)  # creating population

selector = Selector(ExternalFactors())  # creating the initial parameters of the population and selector
mutation_mode = NormalMutator()  # mutation mode for bacterias iterations

for _ in range(10):
    iterate(population, selector, mutation_mode).draw()  # drawing a population without saving
