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
        page = HomePage({'params_selected': params_selected,
                         'add': add,
                         'build': build,
                         'reset': reset,
                         'storage_update': storage_update,
                         'figure_update': figure_update
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
