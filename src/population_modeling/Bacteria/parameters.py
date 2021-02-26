from src.population_modeling.Evolution import genome
from src.population_modeling.Population import population


class Parameters:
    """
    Class for description of bacteria's parameters.

    Attributes
    ----------
    genome : genome
        Bacteria's genome parameters
    population : population
        Population in which situated bacteria
    lived_time : int
        Already lived time
    """
    def __init__(self, genome_: genome, population_: population):
        self.genome = genome_
        self.population = population_
        self.lived_time = 0
