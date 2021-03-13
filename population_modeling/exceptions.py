from population_modeling.bacteria import Bacteria


class DeadBacteriaException(Exception):
    """
    Exception class for the case when trying to address a dead bacterium
    """
    def __init__(self, bacteria: Bacteria, message: str = 'Addressing for a dead bacteria'):
        super().__init__(message)
        self.bacteria = bacteria
        self.message = message

    def __str__(self):
        return f'{self.bacteria} -> {self.message}'
