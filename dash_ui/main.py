from dash_ui.ui import DashUI  # type: ignore
from dash_ui import HomePage
from research_ui import ResearchUI  # type: ignore


class App:
    """
        A class that implements the connection between the Dash interface and the Population Research API
        To do this, you need to connect the outputs and inputs of the page with the functions from the API
    """

    def __init__(self) -> None:
        # Create a home page instance and callback implementations link with it
        # ResearchUI(... :Research)
        research_callbacks = ResearchUI()
        page = HomePage(research_callbacks.get_callbacks_dict())

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
