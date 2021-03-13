from population_modeling.bacteria import Bacteria
import igraph  # type: ignore


class Population:
    """
    A class containing information about the population. An iterator is implemented using a class Population.Iterator.
    Bacteria can get information about their population to adjust their behavior

    Parameters
    ----------
    genealogical_tree: igraph.Graph
        Structure of the population

    Returns
    -------
    Bacteria
        Bacteria with set parameters
    """
    INDIVIDUAL_KEY = 'bacteria'
    GENERATION_KEY = 'generation'

    def __init__(self, genealogical_tree: igraph.Graph):
        self.genealogical_tree = genealogical_tree


def create_graph(first_bacteria: Bacteria) -> igraph.Graph:
    """
    Create new graph with one node and two labels

    :param first_bacteria: label of the node
    :return: graph
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


def draw(population: Population, filename: str = None) -> None:
    """

    Fuctions, that implement drawing of Population instance in tree form.

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
        vertex_color=['green' if node[Population.INDIVIDUAL_KEY].is_alive else 'red'
                      for node in population.genealogical_tree.vs]
    )
