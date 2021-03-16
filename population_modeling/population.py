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

    def draw(self, filename: str = None) -> None:
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

        layout = self.genealogical_tree.layout_reingold_tilford(root=[0])
        igraph.plot(
            self.genealogical_tree,
            filename,
            layout=layout,
            vertex_label=[node.index for node in self.genealogical_tree.vs],
            bbox=(600, 600),
            vertex_color=['green' if node[Population.INDIVIDUAL_KEY].is_alive() else 'red'
                          for node in self.genealogical_tree.vs]
        )


def create_graph(first_bacteria: Bacteria) -> igraph.Graph:
    """
    Create new graph with one node and two labels

    Parameters
    ----------
    first_bacteria: Bacteria
        Bacteria that is the basis for the graph

    Returns
    -------
    igraph.Graph
        New graph
    """

    graph = igraph.Graph(directed=True)
    graph.add_vertex(bacteria=first_bacteria, generation= 0)

    return graph


def create_population(first_bacteria: Bacteria) -> Population:
    """
    Simple creating population from one bacteria

    Parameters
    ----------
    first_bacteria: Bacteria
        Bacteria class instance

    Returns
    -------
        Population
    """

    genealogical_tree = create_graph(first_bacteria)  # TODO add multiple bacteria for initialization

    return Population(genealogical_tree)
