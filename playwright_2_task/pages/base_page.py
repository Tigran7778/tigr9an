from playwright.sync_api import Page
from configs.config_reader import ConfigReader


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.config = ConfigReader()
