from abc import abstractmethod
from typing import List
import dash_html_components as html  # type: ignore
from dash_ui import Callback


class AbstractPage:
    """
        Abstract page that declares the interface of the pages
        Pages should give their callbacks and their dash.Html template

        Methods
        -------
        get_layout(self) -> html:
            Returns the page template


    """
    def __init__(self, functions: dict, callbacks: dict):
        self._callbacks = _init_callbacks(functions, callbacks)

    @abstractmethod
    def get_layout(self) -> html:
        """
        Returns the page template
        """
        raise NotImplementedError

    @abstractmethod
    def get_callbacks(self) -> List[Callback]:
        """
        Returns callbacks that are bound to the page
        """
        raise NotImplementedError


def _init_callbacks(functions: dict, callbacks: dict) -> dict:
    """
    Links functions and callbacks by keys in dictionaries

    Parameters
    ----------
    functions: dict
        functions dict
    callbacks
        callbacks dict
    Returns
    -------
        list of callbacks with saved functions
    """
    for key in callbacks.keys():
        callbacks[key].set_func(functions[key])

    return callbacks

