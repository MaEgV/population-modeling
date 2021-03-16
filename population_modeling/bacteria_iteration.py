from typing import List

from population_modeling.bacteria import Bacteria
from population_modeling.exceptions import DeadBacteriaException
from population_modeling.selector import Selector
from population_modeling.mutations import MutationalProcesses


def iterate(selector: Selector, mutation_mode: MutationalProcesses, bacteria: Bacteria) -> list:
    """

    Function that implements a single time cycle of a bacterium, during which it can die or multiply

    Parameters
    ----------
    mutation_mode: MutationalProcesses
        Implementation of mutation mechanisms

    bacteria: Bacteria
        Instance of the class Bacteria which iterated

    selector: Selector
        Decide fate of bactria

    Returns
    -------
    list
        List of child's if they are, if Bacteria not alive returns empty list

    """
    if not bacteria.is_alive():
        raise DeadBacteriaException(bacteria)

    mutation_mode.mutation(bacteria.genome)

    if selector.is_died(bacteria.genome):
        bacteria.die()
        return []

    bacteria.inc_age()

    return _get_children(selector, mutation_mode, bacteria)


def _get_children(selector: Selector, mutation_mode: MutationalProcesses, bacteria: Bacteria) -> List[Bacteria]:
    """
    Generate bacteria's children

    Parameters
    ----------
    mutation_mode:
        Implementation of mutation mechanisms

    bacteria: Bacteria
        A bacterium whose descendants may appear

    selector: Selector
        Make decisions about bacteria's future actions

    Returns
    -------
    list[Bacteria]
        Bacteria's children (if they are be)

    """

    children = list()
    while selector.have_to_reproduct(bacteria.genome):  # the Bernoulli test
        child_genome = mutation_mode.child_genome(bacteria.genome)
        children.append(Bacteria(child_genome))

    return children
