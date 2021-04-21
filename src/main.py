from ui.ui import DashUI
from src.ui.pages.Home.home_page import HomePage
from callback_logic import *


class App:
    def __init__(self):
        tmp = HomePage({'counter': individual_counter,
                        'add': add,
                        'build': build,
                        'selector_cfg': selector_cfg,
                        'mutator_cfg': mutator_cfg,
                        'individual_cfg': ndividual_cfg,
                        'rebuild': rebuild
                        })

        self.ui = DashUI(tmp)

    def run(self):
        self.ui.run()


if __name__ == "__main__":
    App().run()
