from playwright.sync_api import Page
from .base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # локаторы находящиеся на главной странице
        self.search_input = self.page.get_by_role("textbox", name="Search")
        self.search_button = self.page.get_by_role("button", name="Search")

    def search_article(self, name=None):
        if name is None:
            name = "Default Name"
        self.search_input.fill(name)
        self.search_button.click()

    def open(self, url):
        self.page.goto(url)
