from ui.ui import DashUI
from src.ui.pages.Home.home_page import HomePage
from callback_logic import *


class App:
    """
        A class that implements the connection between the Dash interface and the Population Research API
        To do this, you need to connect the outputs and inputs of the page with the functions from the API
    """
    def __init__(self):
        # Create a home page instance and callback implementations link with it
        page = HomePage({'counter': individual_counter,
                        'add': add,
                        'build': build,
                        'selector_cfg': selector_cfg,
                        'mutator_cfg': mutator_cfg,
                        'individual_cfg': ndividual_cfg,
                        'rebuild': rebuild
                        })

        # Creating a Dash app for a page
        self.ui = DashUI(page)

    def run(self) -> None:
        """
        Launch app
        Returns
        -------
        None
        """
        self.ui.run()


if __name__ == "__main__":
    App().run()
