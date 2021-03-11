from population_modeling.bacteria import create_bacteria, Selector
import igraph # type: ignore


def create_graph(first_bacteria):
    '''
    Create new graph with one node and two labels

    :param first_bacteria: label of the node
    :return: graph
    '''
    graph = igraph.Graph(directed=True)
    graph.add_vertex(bacteria=first_bacteria, generation=0)

    return graph


class Population:
    """
    A class containing information about the population. An iterator is implemented using a class Population.Iterator.
    Bacteria can get information about their population to adjust their behavior

    Attributes
    ----------
    selector_: Selector
        an instance of the selection class that includes the initial parameters
        of the living conditions in the populatio
    max_life_time: int
        max life time of first bacteria
    p_for_death: float
        probability for death per iteration of first bacteria
    p_for_reproduction: float
        probability for reproduce 1 child per iteration of first bacteria (could be many children)

    Methods
    -------
    __iter__(self) -> Iterator:
        get iterator of Population
    """
    INDIVIDUAL_KEY = 'bacteria'
    GENERATION_KEY = 'generation'

    def __init__(self, selector_: Selector, max_life_time=5, p_for_death=0.5, p_for_reproduction=0.5):
        self.selector = selector_
        self.graph = create_graph(create_bacteria(max_life_time, p_for_death, p_for_reproduction))

    def iteration(self):
        '''
        Iteration of population. Call bacterias method @iteration@ and process children
        :return: self
        '''
        new_generation = list()
        for vertex in self.graph.vs:
            parent = vertex[Population.INDIVIDUAL_KEY]  # Get the object of the bacterium from the node

            if parent.is_alive:
                children = parent.iteration(self.selector)

                if children:
                    new_generation.append((vertex, children))

        self._process_new_generation(new_generation)
        self._update_properties()

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
        self.graph.add_vertices(
            len(children),
            {Population.INDIVIDUAL_KEY: children,
             Population.GENERATION_KEY: [parent[Population.GENERATION_KEY] + 1] * len(children)}
        )

        # Add directed edges from parent to children
        self.graph.add_edges([(parent, child) for child in self.graph.vs[-len(children)::]])

    def _update_properties(self) -> None:
        '''
        IN PROGRESS
        Recounting external factors after iteration. Changing living conditions
        Returns None
        '''
        self.selector.external_factors.antagonism = 0  # temporary solution
        self.selector.external_factors.overpopulation = 0  # temporary solution

    def draw(self, filename=None):
        '''
        Drawing directed graph with reingold layout and show in png format
        :return: None
        '''
        layout = self.graph.layout_reingold_tilford(root=[0])
        igraph.plot(
            self.graph,
            filename,
            layout=layout,
            vertex_label=[node.index for node in self.graph.vs],
            bbox=(600, 600),
            vertex_color=['green' if node[Population.INDIVIDUAL_KEY].is_alive else 'red' for node in self.graph.vs]
        )
