import dash_html_components as html
import dash_core_components as dcc
from ui.ui import DashUI
from src.ui.pages.Home.home_page import HomePage
from callback_logic import *

def t():
    return [-100]

class App:
    def __init__(self):
        tmp = HomePage([update_output, add, t])
        self.ui = DashUI(tmp)

    def run(self):
        self.ui.run()


if __name__ == "__main__":
    App().run()
