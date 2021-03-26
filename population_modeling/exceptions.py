class DeadBacteriaException(Exception):
    """
    Exception class for the case when trying to address a dead bacterium

    """
    def __init__(self, bacteria_str: str, message: str = 'Addressing for a dead bacteria'):
        super().__init__(message)
        self.bacteria = bacteria_str
        self.message = message

    def __str__(self) -> str:
        return f'{self.bacteria} -> {self.message}'
