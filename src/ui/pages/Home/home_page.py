import dash_html_components as html  # type: ignore
from ..abstract_page import AbstractPage
from .home_template import HomeTemplate


def _init_id() -> str:
    """
    Function that returns the home page id
    Returns
    -------
        str:
            id
    """
    last_id = 0

    def get_id():
        nonlocal last_id
        last_id += 1
        return last_id - 1

    return f'home_temp_{get_id()}'


class HomePage(AbstractPage):
    """
        Implementation of the AbstractPage class for the home page

        Attributes
        ----------
        _template
        Methods
        -------
        get_layout(self) -> html.Div:
            Returns the home page template

        get_callbacks(self):
            Returns the home page callbacks
    """
    _template: HomeTemplate = HomeTemplate()

    def __init__(self, functions: dict):
        super().__init__(functions, HomePage._template.get_callbacks())
        self.id = _init_id()

    def get_layout(self) -> html.Div:
        """
        Returns the home page template
        """
        return html.Div(
                id=self.id,
                children=HomePage._template.get_children()
           )

    def get_callbacks(self) -> list:
        """
        Returns the home page callbacks
        """
        return list(self._callbacks.values())
