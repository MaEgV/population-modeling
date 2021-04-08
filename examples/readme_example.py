from population_modeling import *
from population_modeling.statistic import Statistics

first_bacteria = create_bacteria(p_for_death=0.1, p_for_reproduction=0.8)  # creating first bacteria to start a population
population = create_population(first_bacteria)  # creating population

cycle = LifeCycle(population)  # main cycle

stats = Statistics(cycle)
data = stats.num_of_individuals(4, selector='DefaultSelector', mutator=NormalMutator(), loc=1, scale=0)
print(data)

# for _ in range(10):
    # cycle.iterate(selector, mutation_mode, draw_func=draw)  # drawing a population without saving

