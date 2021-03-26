from population_modeling import *

first_bacteria = create_bacteria(p_for_death=0.1, p_for_reproduction=0.5)  # creating first bacteria to start a population
population = create_population(first_bacteria)  # creating population


selector_params = SelectorParams(0, 1)  # choose parameters for selection
selector = DefaultSelector(selector_params, ExternalFactors())  # creating the initial parameters of the population and selector
mutation_mode = NormalMutator()  # mutation mode for bacterias iterations

cycle = LifeCycle(population)  # main cycle

for _ in range(10):
    cycle.iterate(selector, mutation_mode, draw_func=draw)  # drawing a population without saving
