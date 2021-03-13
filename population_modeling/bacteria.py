from population_modeling.selector import Selector, Genome
from population_modeling.exceptions import DeadBacteriaException
from population_modeling.mutations import MutationalProcesses, NormalMutations


class Bacteria:
    """
       Represents bacteria with its parameters

       Attributes
       ----------
       is_alive : bool
           Is bacteria alive or dead
       genome : Genome
           Genome of bacteria

       Methods
       -------

        get_children(self, selector: Selector) -> list
            Generate children
       """

    def __init__(self, genome: Genome):
        self.is_alive = True
        self.age = 0
        self.genome = genome


def get_children(selector: Selector, mutation_mode: MutationalProcesses, bacteria: Bacteria) -> list:
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


def iteration(selector: Selector, mutation_mode: MutationalProcesses, bacteria: Bacteria) -> list:
    """

        In method selector decide fate of bactria: should it die or should it reproduct

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
    if not bacteria.is_alive:
        raise DeadBacteriaException(bacteria)

    mutation_mode.mutation(bacteria.genome)

    if bacteria.age > bacteria.genome.max_life_time or selector.is_died(bacteria.genome):
        bacteria.is_alive = False
        return []

    bacteria.age += 1

    return get_children(selector, mutation_mode, bacteria)


def create_bacteria(max_life_time=5, p_for_death=0.5, p_for_reproduction=0.5) -> Bacteria:
    """

    Create bacteria from different parameters

    Parameters
    ----------
    max_life_time: int
        Maximum iterations for bacteria
    p_for_death: float
        Probability of death
    p_for_reproduction: float
        Probability of reproduction

    Returns
    -------
    Bacteria
        Bacteria with set parameters

    """

    return Bacteria(Genome(max_life_time, p_for_death, p_for_reproduction))
