from population_modeling import create_bacteria, create_population, SelectorParams, NormalMutator, LifeCycle, \
    DefaultSelector, ExternalFactors
from population_modeling.ui.ui import DashUI
from population_modeling.statistic import Statistics



first_bacteria = create_bacteria(p_for_death=0.5, p_for_reproduction=0.5)  # creating first bacteria to start a population

selector_params = SelectorParams(0, 1)  # choose parameters for selection
selector = DefaultSelector(selector_params,
                           ExternalFactors())  # creating the initial parameters of the population and selector
mutation_mode = NormalMutator()  # mutation mode for bacterias iterations

cycle = LifeCycle(create_population(first_bacteria))  # main cycle


def create_callback1(stats: Statistics):
    def func(n_clicks, value):
        print(1)
        cycle = LifeCycle(create_population(create_bacteria(p_for_death=0.5, p_for_reproduction=0.5)))  #
        data_creator = Statistics(cycle)
        return data_creator.num_of_individuals(20, selector, mutation_mode)

    return func

class App:
    def __init__(self):
        self.data_creator = Statistics(cycle)
        self.ui = DashUI({'button': create_callback1(self.data_creator)})

    def run(self):
        self.ui.run()



if __name__ == "__main__":
    App().run()
