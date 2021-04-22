from typing import List, Any
import dash  # type: ignore
from .callback import Callback
from .pages.abstract_page import AbstractPage


class DashUI:
    """
        A dash application UI class that allows you to start the server and display the AbstractPage implementation

        Attributes
        ----------
        app: dash.Dash

        Methods
        -------
    """
    def __init__(self, page: AbstractPage):
        self.app = dash.Dash(__name__)
        self.app.layout = page.get_layout()

        register_callbacks(self.app, page.get_callbacks())

    def run(self, debug: bool = True, host: str = '127.0.0.1') -> None:
        """
        Launch the Dash app

        Parameters
        ----------
        debug:
            Launch mode
        host:
            Launch host
        Returns
        -------
        None
        """
        self.app.run_server(debug=debug, host=host)


def register_callbacks(app: dash.Dash, callbacks: List[Callback]) -> None:
    """
    A function that registers callbacks in the Dash app

    Parameters
    ----------
    app
        The application to register with

    callbacks
        Sausages that need to be registered

    Returns
    -------
    None
    """
    for callback in callbacks:
        add_callback(app, callback)


def add_callback(app: dash.Dash, callback: Callback) -> None:
    """
    A function that registers single callback in the Dash app

    Parameters
    ----------
    app
        The application to register with

    callback
        Sausages that need to be registered

    Returns
    -------
    None
    """
    @app.callback(callback.get_args(), **callback.get_kwargs())
    def inner(*args: tuple, **kwargs: dict) -> Any:
        return callback.get_func()(*args, **kwargs)
