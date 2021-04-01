from population_modeling.bacteria import Bacteria
from typing import ClassVar, Any
from dataclasses import dataclass
import networkx as nx  # type: ignore
import matplotlib.pyplot as plt


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

    genealogical_tree: nx.DiGraph
    INDIVIDUAL_KEY: ClassVar[str] = 'bacteria'
    GENERATION_KEY: ClassVar[str] = 'generation'

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
        last_id = len(self.genealogical_tree.nodes)
        for parent, children in new_generation:
            for child in children:
                self.genealogical_tree.add_node(last_id + 1, bacteria=child)
                self.genealogical_tree.add_edge(parent, last_id + 1)
                last_id += 1


    # def _process_offspring(self, parent: igraph.Graph.vs, children: list) -> None:
    #     """
    #     Processing parent-child pairs
    #
    #     Parameters
    #     ----------
    #     population: Population
    #         Processed population
    #
    #     parent: igraph.Graph.vs
    #         Parent-graph
    #
    #     children: list
    #         List of new children, which should be added to graph
    #
    #     Returns
    #     -------
    #     None
    #
    #     """
    #
    #     # Add children to graph vertices with new generation labels
    #     self.genealogical_tree.add_vertices(
    #         len(children),
    #         {Population.INDIVIDUAL_KEY: children,
    #          Population.GENERATION_KEY: [parent[Population.GENERATION_KEY] + 1] * len(children)}
    #     )
    #
    #     # Add directed edges from parent to children
    #     self.genealogical_tree.add_edges(
    #         [(parent, child) for child in self.genealogical_tree.vs[-len(children)::]]
    #     )


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

    # layout = population.genealogical_tree.layout_reingold_tilford(root=[0])
    print(len(population.genealogical_tree.nodes))
    nx.draw(population.genealogical_tree)
    plt.show()

    # nx.plot(
    #     population.genealogical_tree,
    #     filename,
    #     layout=layout,
    #     vertex_label=[node.index for node in population.genealogical_tree.vs],
    #     bbox=(600, 600),
    #     vertex_color=['green' if node[Population.INDIVIDUAL_KEY].is_alive() else 'red'
    #                   for node in population.genealogical_tree.vs]
    # )


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
    genealogical_tree = nx.DiGraph()
    genealogical_tree.add_node(0, bacteria=bacteria)

    return Population(genealogical_tree)
