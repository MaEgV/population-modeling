from dataclasses import dataclass


@dataclass
class MutatorParams:
    """

    Dataclass for such mutational parameters as mean(loc) and standard deviation(scale).

    Attributes
    ----------
    loc: float
        Mean

    scale: float
        Standard deviation

    """
    loc: float
    scale: float
