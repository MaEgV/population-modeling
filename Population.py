from Bacteria import create_bacteria
import igraph


def get_new_graph(first_bacteria):
    graph = igraph.Graph(directed=True)
    graph.add_vertex(bacteria=first_bacteria, generation=0)

    return graph


class Population:
    """
    This is a class that contains a set of bacteria in the form of a directed graph.
    Bacterias are linked by a parent-child relationship.
    The implication is that bacteria evolve over time,
    so the population class makes it possible to integrate over time across all individuals.
    In addition, an informative way of drawing all the bacteria is implemented in this class.

    Attributes
    ----------
    n : int
        Max iterations number for iterator
    first_bacteria_genom : dict
        max_life_time_: int, p_for_death_: float, p_for_reproduction_: float)

    Methods
    -------
    """
    INDIVIDUAL_KEY = 'bacteria'
    GENERATION_KEY = 'generation'

    def __init__(self, n=None, max_life_time=5, p_for_death=0.5, p_for_reproduction=0.5):
        self._max_n = n
        self._current_n = 0
        self._first_bacteria = create_bacteria(self, max_life_time, p_for_death, p_for_reproduction)
        self._graph = get_new_graph(self._first_bacteria)

    def __iter__(self):
        self._graph = get_new_graph(self._first_bacteria)
        self._current_n = 0

        return self

    def __next__(self):
        if self._end_iter():
            raise StopIteration

        new_generation = list()
        for vertex in self._graph.vs:
            parent = vertex[Population.INDIVIDUAL_KEY]  # Get the object of the bacterium from the vertex

            if parent.is_alive:
                children = parent.iteration()

                if children:
                    new_generation.append((vertex, children))

        self._process_new_generation(new_generation)

        return self

    def _end_iter(self) -> bool:
        self._current_n += 1

        return self._max_n < self._current_n or self._max_n is None

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
        # Add children to graph vertices
        self._graph.add_vertices(
            len(children),
            {Population.INDIVIDUAL_KEY: children,
             Population.GENERATION_KEY: [parent[Population.GENERATION_KEY] + 1] * len(children)}
        )

        # Add edges from parent to children
        self._graph.add_edges([(parent, child) for child in self._graph.vs[-len(children)::]])

    def draw(self):
        layout = self._graph.layout_reingold_tilford(root=[0])
        igraph.plot(
            self._graph,
            layout=layout,
            vertex_label=[node.index for node in self._graph.vs],
            bbox=(600, 600),
            vertex_color=['green' if node['bacteria'].is_alive else 'red' for node in self._graph.vs]
        )
