class DeadBacteria(Exception):
    def __init__(self, bacteria, message='Addressing for a dead bacteria'):
        super().__init__(message)
        self.bacteria = bacteria  # here will be id
        self.message = message

    def __str__(self):
        return f'{self.bacteria} -> {self.message}'