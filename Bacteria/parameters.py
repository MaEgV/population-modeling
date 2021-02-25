from Evolution import genome
from Population import population


class Parameters:
    """
    Class for description of bacteria's parameters.

    Attributes
    ----------
    genome : пenome
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
