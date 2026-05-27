import logging
import time
from playwright.sync_api import Page
from base_page import BasePage

logger = logging.getLogger(__name__)


class SearchResultsPage(BasePage):
    # XPath локаторы
    SORT_SELECT = '//select[@data-testid="filter-sort"]'
    PRICE_ELEMENTS = '//div[@data-testid and contains(@data-testid, "search-result-price-")]'

    def set_filter(self, filter_type: str) -> None:
        """Выбирает значение фильтра сортировки."""
        logger.info(f"Setting sort filter: '{filter_type}'")

        sort_values = {
            "Price: low to high": "price_asc",
            "Price: high to low": "price_desc",
        }

        value = sort_values.get(filter_type)
        if not value:
            raise ValueError(f"Unknown filter: {filter_type}")

        # Выбираем опцию
        sort_select = self.page.locator(self.SORT_SELECT)
        sort_select.wait_for(state="visible", timeout=10_000)
        sort_select.select_option(value=value)

        # 1. Ждём появления класса is-loading на results-region
        results_region = self.page.locator('[data-testid="results-region"]')
        results_region.wait_for(state="visible", timeout=10_000)
        time.sleep(0.5)

        # 2. Ждём загрузки новых результатов (исчезновения is-loading)
        self.page.wait_for_function(
            """() => {
                const region = document.querySelector('[data-testid="results-region"]');
                return region && !region.classList.contains('is-loading');
            }""",
            timeout=10_000
        )

        # 3. Ждём загрузки сети
        self.page.wait_for_load_state("networkidle", timeout=10_000)

        logger.info(f"Filter '{filter_type}' applied")

    def get_prices(self, n: int) -> list[float]:
        """Считывает цены первых n карточек."""
        logger.info(f"Collecting first {n} prices")

        # ── Ждём первого элемента цены ─────────────────────────────────────────
        price_locator = self.page.locator(self.PRICE_ELEMENTS)
        price_locator.first.wait_for(state="visible", timeout=10_000)

        # ── Даём время на полную загрузку списка ───────────────────────────────
        time.sleep(0.5)

        # ── Собираем цены ─────────────────────────────────────────────────────
        all_elements = price_locator.all()
        prices: list[float] = []

        for element in all_elements[:n]:
            raw = element.get_attribute("data-price")
            if raw is not None:
                try:
                    # Делим на 100, так как цена хранится в копейках
                    prices.append(int(raw) / 100)
                except ValueError:
                    logger.warning(f"Cannot parse data-price='{raw}'")

        logger.info(f"Prices collected ({len(prices)}): {prices}")
        return prices
