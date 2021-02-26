from Bacteria.bacteria import Bacteria
import igraph


def create_graph(first_bacteria):
    '''
    Create new graph with one node and two labels

    :param first_bacteria: label of the node
    :return: graph
    '''
    graph = igraph.Graph(directed=True)
    graph.add_vertex(bacteria=first_bacteria, generation=0)

    return graph


class Iterator:
    """
    A class that iterates through a population consisting of a single bacterium.
    First bacterium provides information about the Population class, witch saved by Iterator.
    It allows to change the state of the class after each iteration.
    All individuals are stored as a directed graph. It is possible to draw a population graph.

    Attributes
    ----------
    max_iter: int
        max iterations number
    first_bacteria: Bacteria
        first individual in population

    Methods
    -------
    __next(self)__ -> Iterator:
        one iteration. calling @iteration@ for each bacteria in population and adding children to population graph
    """
    INDIVIDUAL_KEY = 'bacteria'
    GENERATION_KEY = 'generation'

    def __init__(self, max_iter: int, first_bacteria: Bacteria):
        self.n = max_iter  # max number of iterations
        self._graph = create_graph(first_bacteria)  # structure with bacteria population
        self.population = first_bacteria.parameters.population

    def __next__(self):
        '''
        Iteration of population. Call bacterias method @iteration@ and process children
        :return: self
        '''
        if self._end_iter():
            raise StopIteration

        new_generation = list()
        for vertex in self._graph.vs:
            parent = vertex[Iterator.INDIVIDUAL_KEY]  # Get the object of the bacterium from the node

            if parent.is_alive:
                children = parent.iteration()

                if children:
                    new_generation.append((vertex, children))

        self._process_new_generation(new_generation)

        return self

    def _process_new_generation(self, new_generation: list):
        """
        Wrapper for processing parent-child pairs

        :param new_generation: list(tuple(Vertice, list(Bacteria)))
            Contain pairs parant:children
        :return: None
        """
        for parent, children in new_generation:
            self._process_offspring(parent, children)

    def _process_offspring(self, parent, children: list) -> None:
        """
        Processing parent-child pairs

        :param parent: Vertices
        :param children: list(Bacteria)
        :return: None
        """
        # Add children to graph vertices with new generation labels
        self._graph.add_vertices(
            len(children),
            {Iterator.INDIVIDUAL_KEY: children,
             Iterator.GENERATION_KEY: [parent[Iterator.GENERATION_KEY] + 1] * len(children)}
        )

        # Add directed edges from parent to children
        self._graph.add_edges([(parent, child) for child in self._graph.vs[-len(children)::]])

    def _end_iter(self) -> bool:
        '''
        Determines whether to stop iterations
        :return: bool
        '''
        self.n -= 1

        return self.n < 0

    def draw(self, filename=None):
        '''
        Drawing directed graph with reingold layout and show in png format
        :return: None
        '''
        layout = self._graph.layout_reingold_tilford(root=[0])
        igraph.plot(
            self._graph,
            filename,
            layout=layout,
            vertex_label=[node.index for node in self._graph.vs],
            bbox=(600, 600),
            vertex_color=['green' if node[Iterator.INDIVIDUAL_KEY].is_alive else 'red' for node in self._graph.vs]
        )
