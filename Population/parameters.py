from scipy.stats import norm


class Parameters:
    def __init__(self, max_population=50, antagonism=0, overpopulation=0):
        self._max_population = max_population

        self.antagonism = antagonism  # may be negative (collaboration)
        self.overpopulation = overpopulation

    def refresh_overpopulation(self, current_population: int) -> None:
        '''
        EXAMPLE FUNCTIONS: updates overpopulation value of population
        :param current_population: number of live bacteria
        '''
        self.overpopulation = (self._max_population - current_population) / self._max_population / 20

    def refresh_antagonism(self) -> None:
        '''
        EXAMPLE FUNCTIONS: updates antagonism value of population
        '''
        self.antagonism = max(min(self.antagonism + norm.cdf(0, 0.005), 1), -1)