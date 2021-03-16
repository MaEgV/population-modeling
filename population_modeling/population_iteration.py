from population_modeling.population import Population, igraph
from population_modeling.selector import Selector
from population_modeling.mutations import MutationalProcesses
from population_modeling.bacteria_iteration import iterate as iterate_bacteria


def iterate(population: Population, selector: Selector, mutation_mode: MutationalProcesses) -> Population:
    """
    Iteration of population. Call bacterias iterations and process children - append new generation at genealogical
    tree.

    Parameters
    ----------
    population: Population
        Iterable population

    selector: Selector
        Selector with preferred methods

    mutation_mode: MutationalProcesses
        Preferred type of mutations

    Returns
    -------
    Population
        Changed population

    """

    new_generation = list()
    for vertex in population.genealogical_tree.vs:
        parent = vertex[Population.INDIVIDUAL_KEY]  # Get the object of the bacterium from the node

        if parent.is_alive():
            children = iterate_bacteria(selector, mutation_mode, parent)

            if children:
                new_generation.append((vertex, children))

    _process_new_generation(population, new_generation)
    _update_properties(population, selector)

    return population


def _process_new_generation(population: Population, new_generation: list) -> None:
    """
    Wrapper for processing parent-child pairs.

    Parameters
    ----------
    population: Population
        Processed population

    new_generation: list
        Contain pairs parent: children

    Returns
    -------
    None

    """
    for parent, children in new_generation:
        _process_offspring(population, parent, children)


def _process_offspring(population: Population, parent: igraph.Graph.vs, children: list) -> None:
    """
    Processing parent-child pairs

    Parameters
    ----------
    population: Population
        Processed population

    parent: igraph.Graph.vs
        Parent-graph

    children: list
        List of new children, which should be added to graph

    Returns
    -------
    None

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

    Parameters
    ----------
    population: Population
        Processed population

    selector: Selector
        Required selector

    Returns
    -------
    None
    """

    selector.external_factors.antagonism = 0  # TODO: add logic
    selector.external_factors.overpopulation = 0  # TODO: add logic