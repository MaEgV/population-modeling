from population_modeling.population import Population
from population_modeling.selector import Selector, ExternalFactors
from population_modeling.mutations import MutationalProcesses, NormalMutations
from population_modeling.bacteria_iteration import iterate as iterate_bacteria


def iterate(population: Population, selector: Selector, mutation_mode: MutationalProcesses):
    """
    Iteration of population. Call bacterias iterations and process children - append new generation at genealogical tree
    :return: self
    """
    new_generation = list()
    for vertex in population.genealogical_tree.vs:
        parent = vertex[Population.INDIVIDUAL_KEY]  # Get the object of the bacterium from the node

        if parent.is_alive:
            children = iterate_bacteria(selector, mutation_mode, parent)

            if children:
                new_generation.append((vertex, children))

    _process_new_generation(population, new_generation)
    _update_properties(population, selector)

    return population


def _process_new_generation(population: Population, new_generation: list):
    """
    Wrapper for processing parent-child pairs

    :param new_generation: list
        Contain pairs parent: children
    :return: None
    """
    for parent, children in new_generation:
        _process_offspring(population, parent, children)


def _process_offspring(population: Population, parent, children: list) -> None:
    """
    Processing parent-child pairs

    :param parent: Vertices
    :param children: list(Bacteria)
    :return: None
    """
    # Add children to graph vertices with new generation labels
    population.genealogical_tree.add_vertices(
        len(children),
        {Population.INDIVIDUAL_KEY: children,
         Population.GENERATION_KEY: [parent[Population.GENERATION_KEY] + 1] * len(children)}
    )

    # Add directed edges from parent to children
    population.genealogical_tree.add_edges(
        [(parent, child) for child in population.genealogical_tree.vs[-len(children)::]]
    )


def _update_properties(population: Population, selector: Selector) -> None:
    """
    IN PROGRESS
    Recounting external factors after iteration. Changing living conditions
    Returns None
    """
    selector.external_factors.antagonism = 0  # TODO: add logic
    selector.external_factors.overpopulation = 0  # TODO: add logic
