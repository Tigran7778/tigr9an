from .base_page import BasePage
from playwright.sync_api import Page


class SearchResultsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Локаторы в init
        self.price_locator = self.page.locator('//div[@data-testid and contains(@data-testid, "search-result-price-")]')
        self.filter_select_locator = self.page.locator('//select[@data-testid="filter-sort"]')

    def get_prices(self, n):
        return [float(self.price_locator.nth(i).inner_text().replace('RUB', '').strip()) for i in range(n)]

    def apply_filter(self, filter_type):
        filter_select = self.filter_select_locator
        if filter_select.count() > 0:
            filter_select.select_option(label=filter_type)
        else:
            raise ValueError(f"Filter '{filter_type}' not found.")
