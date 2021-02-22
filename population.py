from queue import Queue
from Bacteria import Bacteria
import igraph
import BacteriaParameters


def traversal(graph: igraph.Graph):
    queue = Queue()
    queue.put(0)
    visited_nodes = {0}

    while True:
        u = queue.get()
        yield graph.vs[u]

        for node in graph.neighbors(u):
            if node not in visited_nodes:
                visited_nodes.add(node)
                queue.put(node)

        if queue.empty():
            break


class Population:
    def __init__(self, n: int, first_bacteria: Bacteria):
        self._graph = igraph.Graph(directed=True)
        self._graph.add_vertex(bacteria=first_bacteria, generation=0)
        self._n = n

    def process_offspring(self, offspring, father):
        self._graph.add_vertices(
            len(offspring),
            {'bacteria': offspring, 'generation': [father['generation']+1]*len(offspring)}
        )

        new_vertexes = self._graph.vs[-len(offspring)::]
        for child in new_vertexes:
            self._graph.add_edge(father, child)

    def time_iteration(self):
        print(len(self._graph.vs))
        for vertex in traversal(self._graph):
            bacteria = vertex['bacteria']

            if bacteria.is_alive:
                offspring = bacteria.iteration()
                if offspring:
                    self.process_offspring(offspring, vertex)

        return self

    def draw(self):
        layout = self._graph.layout_reingold_tilford(root=[0])
        igraph.plot(self._graph, layout=layout)
