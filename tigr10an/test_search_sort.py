import pytest
import logging
from playwright.sync_api import sync_playwright
from config_reader import ConfigReader
from main_page import MainPage
from search_results_page import SearchResultsPage

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("name,n,filter_type", [
    ("city", 10, "Price: low to high"),
    ("city", 15, "Price: high to low"),
    ("habits", 10, "Price: low to high"),
    ("habits", 15, "Price: high to low"),
])
def test_search_and_filter(name, n, filter_type):
    """
    Тест сортировки цен на странице результатов поиска.

    Сценарий:
      1. Открить главную страницу.
      2. Ввести поисковый запрос.
      3. Перейти на страницу результатов.
      4. Установить фильтр сортировки.
      5. Собрать цены первых n товаров.
      6. Проверить, что цены отсортированы правильно.
    """
    logger.info(f"▶ START | name='{name}' | n={n} | filter='{filter_type}'")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # ── Шаг 1-2: Открить главную страницу и ввести запрос ────────────
            main_page = MainPage(page)  # ✅ ТОЛЬКО page!
            main_page.open()
            main_page.search(name)

            # ── Шаг 3-4: Установить фильтр ─────────────────────────────────────
            results_page = SearchResultsPage(page)
            results_page.set_filter(filter_type)

            # ── Шаг 5: Собрать цены ────────────────────────────────────────────
            prices = results_page.get_prices(n)

            assert len(prices) > 0, (
                f"Не удалось собрать цены.\n"
                f"  Запрос: '{name}'\n"
                f"  Проверьте XPath: //div[contains(@data-testid,'article-price-')]"
            )

            logger.info(f"  Collected {len(prices)} prices: {prices}")

            # ── Шаг 6: Проверить сортировку ────────────────────────────────────
            if filter_type == "Price: low to high":
                expected = sorted(prices)
                assert prices == expected, (
                    f"[FAIL] Цены НЕ отсортированы по возрастанию.\n"
                    f"  Запрос: '{name}', n={n}\n"
                    f"  Получено:  {prices}\n"
                    f"  Ожидалось: {expected}"
                )
                logger.info("✅ PASS | Sorted: low → high")

            elif filter_type == "Price: high to low":
                expected = sorted(prices, reverse=True)
                assert prices == expected, (
                    f"[FAIL] Цены НЕ отсортированы по убыванию.\n"
                    f"  Запрос: '{name}', n={n}\n"
                    f"  Получено:  {prices}\n"
                    f"  Ожидалось: {expected}"
                )
                logger.info("✅ PASS | Sorted: high → low")

        finally:
            page.close()
            browser.close()