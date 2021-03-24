from population_modeling.bacteria import Bacteria
from typing import ClassVar
from dataclasses import dataclass
import igraph  # type: ignore


@dataclass(frozen=True)
class Population:
    """
    A class containing information about the population. An iterator is implemented using a class Population.Iterator.
    Bacteria can get information about their population to adjust their behavior

    Parameters
    ----------
    genealogical_tree: igraph.Graph
        Structure of the population

    Methods
    -------
    draw(self, filename: str = None) -> None
        Drawing of population-graph
    """

    genealogical_tree: igraph.Graph
    INDIVIDUAL_KEY: ClassVar[str] = 'bacteria'
    GENERATION_KEY: ClassVar[str] = 'generation'

    def __getitem__(self, key):
        return self.genealogical_tree.vs[Population.INDIVIDUAL_KEY][key]

    def add(self, new_generation: list) -> None:
        """
        Wrapper for processing parent-child pairs.

        Parameters
        ----------
        population: Population
            Processed population

        new_generation: list
            Contain pairs parent-children

        Returns
        -------
        None

        """
        for parent, children in new_generation:
            parent_vs = self.genealogical_tree.vs.find(**{Population.INDIVIDUAL_KEY: parent})
            self._process_offspring(parent_vs, children)

    def _process_offspring(self, parent: igraph.Graph.vs, children: list) -> None:
        """
        Processing parent-child pairs

        Parameters
        ----------
        population: Population
            Processed population

        parent: igraph.Graph.vs
            Parent-graph

        children: list
            List of new children, which should be added to graph

        Returns
        -------
        None

        """

        # Add children to graph vertices with new generation labels
        self.genealogical_tree.add_vertices(
            len(children),
            {Population.INDIVIDUAL_KEY: children,
             Population.GENERATION_KEY: [parent[Population.GENERATION_KEY] + 1] * len(children)}
        )

        # Add directed edges from parent to children
        self.genealogical_tree.add_edges(
            [(parent, child) for child in self.genealogical_tree.vs[-len(children)::]]
        )


def draw(population: Population, filename: str = None) -> None:
    """
    Method, that implement drawing of Population instance in tree form.

    Parameters
    ----------
    population: Population
        witch population should be drawn

    filename: str
        the name of the file to save the drawing to

    Returns
    -------
    None

    """

    layout = population.genealogical_tree.layout_reingold_tilford(root=[0])
    igraph.plot(
        population.genealogical_tree,
        filename,
        layout=layout,
        vertex_label=[node.index for node in population.genealogical_tree.vs],
        bbox=(600, 600),
        vertex_color=['green' if node[Population.INDIVIDUAL_KEY].is_alive() else 'red'
                      for node in population.genealogical_tree.vs]
    )


def create_population(bacteria: Bacteria) -> Population:
    """
    Simple creating population from one bacteria

    Parameters
    ----------
    bacteria: Bacteria
        Bacteria class instance

    Returns
    -------
        Population
    """
    genealogical_tree = igraph.Graph(directed=True)
    genealogical_tree.add_vertex(bacteria=bacteria, generation=0)

    return Population(genealogical_tree)
