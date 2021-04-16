from dataclasses import dataclass, field

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
    _individuals: list = field(default_factory=list)

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
        self._individuals.extend(new_generation)

    def get_all(self):
        return self._individuals

    def get_alive(self):
        return list(filter(lambda x: x.is_alive(), self._individuals))

    def get_dead(self):
        return list(filter(lambda x: not x.is_alive(), self._individuals))
