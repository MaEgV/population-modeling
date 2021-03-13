from population_modeling.bacteria import Bacteria
import igraph  # type: ignore


def create_graph(first_bacteria) -> igraph.Graph:
    """
    Create new graph with one node and two labels

    :param first_bacteria: label of the node
    :return: graph
    """
    graph = igraph.Graph(directed=True)
    graph.add_vertex(bacteria=first_bacteria, generation=0)

    return graph


def create_population(first_bacteria: Bacteria):
    genealogical_tree = create_graph(first_bacteria)  # TODO add multiple bacteria for initialization

    return Population(genealogical_tree)


class Population:
    """
    A class containing information about the population. An iterator is implemented using a class Population.Iterator.
    Bacteria can get information about their population to adjust their behavior

    Parameters
    ----------
    params: PopulationParams
        Class parameters-container

    Returns
    -------
    Bacteria
        Bacteria with set parameters
    """
    INDIVIDUAL_KEY = 'bacteria'
    GENERATION_KEY = 'generation'

    def __init__(self, genealogical_tree: igraph.Graph):
        self.genealogical_tree = genealogical_tree


def draw(population: Population, filename=None):
    '''
    Drawing directed graph with reingold layout and show in png format
    :return: None
    '''
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
