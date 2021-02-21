import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
from Bacteria import Bacteria


def traversal(graph: nx):
    queue = Queue()
    queue.put(0)
    visited_nodes = {0}

    while True:
        u = queue.get()
        yield u

        for node in graph.neighbors(u):
            if node not in visited_nodes:
                visited_nodes.add(node)
                queue.put(node)

        if queue.empty():
            break


class Population:
    def __init__(self, n: int, first_bacteria: Bacteria):
        self._graph = nx.DiGraph()
        self._last_id = 0
        self._graph.add_node(self._last_id, bacteria=first_bacteria)
        self._n = n

    def process_offspring(self, offspring, father_id):
        new_indexes = [self.get_new_id() for _ in range(len(offspring))]
        for child_id, child in zip(new_indexes, offspring):
            self._graph.add_node(child_id, bacteria=child)
            self._graph.add_edge(father_id, child_id)

    def time_iteration(self):
        for index in traversal(self._graph):
            bacteria = self._graph.nodes[index]['bacteria']
            if bacteria.is_alive:
                offspring = bacteria.iteration()
                self.process_offspring(offspring, index)

        return self

    def get_new_id(self):
        self._last_id += 1

        return self._last_id

    def draw(self):
        nx.draw(self._graph)
        plt.show()
