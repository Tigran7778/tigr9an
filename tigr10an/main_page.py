import logging
from playwright.sync_api import Page
from base_page import BasePage
from config_reader import ConfigReader

logger = logging.getLogger(__name__)


class MainPage(BasePage):
    """
    Page Object главной страницы http://144.31.139.115:5000/

    HTML-структура (ключевые элементы):
        <input  data-testid="search-input"  name="q" ...>
        <button data-testid="search-button" type="submit">Search</button>
    """

    # ── XPath локаторы ────────────────────────────────────────────────────────
    SEARCH_INPUT  = '//*[@id="search"]'
    SEARCH_BUTTON = '//button[contains(@data-testid, "search")]'
    # ─────────────────────────────────────────────────────────────────────────

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._base_url: str = ConfigReader().get("app", "base_url")

    def open(self) -> None:
        """Открывает главную страницу и ждёт её загрузки."""
        self.navigate(self._base_url)
        self.wait_for_load()
        logger.info("Main page opened")

    def search(self, query: str) -> None:
        """
        Вводит поисковый запрос в строку поиска и отправляет форму.

        :param query: Текст поискового запроса (например, "city")
        """
        logger.info(f"Typing search query: '{query}'")
        search_input = self.page.locator(self.SEARCH_INPUT)
        search_input.wait_for(state="visible", timeout=10_000)
        search_input.fill(query)

        logger.info("Submitting search form")
        self.page.locator(self.SEARCH_BUTTON).click()
        self.wait_for_load()