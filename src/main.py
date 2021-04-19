from ui.ui import DashUI
from src.ui.pages.Home.home_page import HomePage
from callback_logic import *


class App:
    def __init__(self):
        tmp = HomePage([update_output, add, t])
        self.ui = DashUI(tmp)

    def run(self):
        self.ui.run()



if __name__ == "__main__":
    App().run()
