import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        """Открывает указанный URL."""
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)

    def wait_for_load(self, timeout: int = 10_000) -> None:
        """Ждёт окончания сетевой активности (networkidle)."""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
