from .bacteria import Bacteria
from typing import ClassVar
from dataclasses import dataclass, field
import networkx as nx  # type: ignore


@dataclass
class Population:
    """
    A class containing information about the population. An iterator is implemented using a class Population.Iterator.
    Bacteria can get information about their population to adjust their behavior

    Parameters
    ----------
    genealogical_tree: igraph.Graph
        Structure of the population

    individuals: list
        List with all bacterias

    Methods
    -------
    draw(self, filename: str = None) -> None
        Drawing of population-graph
    """
    individuals: list = field(default_factory=list)

    def add(self, new_generation: list) -> None:
        """
        Wrapper for processing parent-child pairs.

        Attributes
        ----------
        population: Population
            Processed population

        new_generation: list
            Contain pairs parent-children

        Returns
        -------
        None

        """
        self.individuals.extend(new_generation)

    def get_number_individuals(self):
        return len(self.individuals)

    def get_alive_and_dead(self):
        num_alive = 0
        num_dead = 0
        alive = lambda individual: individual.properties.get_is_alive()
        for individual in self.individuals:
            if alive(individual):
                num_alive += 1
            else:
                num_dead += 1
        return num_alive, num_dead
