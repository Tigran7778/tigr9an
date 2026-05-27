import logging
from playwright.sync_api import Page
from base_page import BasePage

logger = logging.getLogger(__name__)


class SearchResultsPage(BasePage):
    """
    Page Object страницы результатов поиска /search?q=...

    HTML-структура (ключевые элементы):
        <!-- Дропдаун сортировки -->
        <select data-testid="sort-select"> ... </select>

        <!-- Карточка товара -->
        <article data-testid="article-card-{N}">
            ...
            <div class="article-price"
                 data-testid="article-price-{N}"
                 data-price="19700">          ← цена в копейках (*100)
                197 RUB
            </div>
        </article>

    Цена читается из атрибута data-price (целое число, равное цене × 100),
    поэтому делим на 100 для получения рублёвого значения.
    """

    # ── XPath локаторы ────────────────────────────────────────────────────────
    SORT_SELECT    = '//select[contains(@data-testid, "filter-sort")]'
    PRICE_ELEMENTS = '//div[contains(@data-testid, "search-result-price")]'
    # ─────────────────────────────────────────────────────────────────────────

    def set_filter(self, filter_type: str) -> None:
        """
        Выбирает значение фильтра сортировки из выпадающего списка.

        :param filter_type: Метка опции ("Price: low to high" / "Price: high to low")
        """
        logger.info(f"Setting sort filter: '{filter_type}'")
        sort_select = self.page.locator(self.SORT_SELECT)
        sort_select.wait_for(state="visible", timeout=10_000)
        sort_select.select_option(label=filter_type, value=filter_type)
        self.wait_for_load()
        logger.info(f"Filter '{filter_type}' applied")

    def get_prices(self, n: int) -> list[float]:
        """
        Считывает цены первых n карточек через атрибут data-price.

        data-price хранит значение умноженное на 100 (например, 19700 → 197.00 RUB),
        поэтому делим на 100.

        :param n: Количество карточек для сбора
        :return:  Список цен в рублях (float)
        """
        logger.info(f"Collecting first {n} prices")
        price_locator = self.page.locator(self.PRICE_ELEMENTS)
        price_locator.first.wait_for(state="visible", timeout=10_000)

        all_elements = price_locator.all()
        prices: list[float] = []

        for element in all_elements[:n]:
            raw = element.get_attribute("data-price")
            if raw is not None:
                try:
                    prices.append(int(raw) / 100)
                except ValueError:
                    logger.warning(f"Cannot parse data-price='{raw}'")

        logger.info(f"Prices collected ({len(prices)}): {prices}")
        return prices