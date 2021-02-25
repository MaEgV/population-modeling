import BacteriaGenome
import Population


class BacteriaParameters:
    """
    Class for description of bacteria's parameters.

    Attributes
    ----------
    genome : BacteriaGenome
        Bacteria's genome parameters
    population : Population
        Population in which situated bacteria
    lived_time : int
        Already lived time
    """
    def __init__(self, genome_: BacteriaGenome, population_: Population):
        self.genome = genome_
        self.population = population_
        self.lived_time = 0




