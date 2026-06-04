import pytest
from playwright.sync_api import sync_playwright
from pages.search_results_page import SearchResultsPage
from pages.main_page import MainPage
from configs.config_reader import ConfigReader


@pytest.mark.parametrize("filter_data", ConfigReader().get_filters())
def test_article_search(filter_data):
    n = filter_data["n"]
    filter_type = filter_data["filter_type"]

    config = ConfigReader()
    url = config.get_url()
    name = config.get_search_name()

    with sync_playwright() as p:
        # Запуск браузера
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Переход на страницу
        page.goto(url)
        page.wait_for_timeout(5000)

        # Создаем объекты страниц
        main_page = MainPage(page)
        results_page = SearchResultsPage(page)

        # Выполнить поиск
        main_page.search_article(name)
        page.wait_for_timeout(5000)

        # Применить фильтр
        results_page.apply_filter(filter_type)
        # Ждем, пока обновится страница после применения фильтра
        page.wait_for_timeout(5000)

        # Получить цены
        prices = results_page.get_prices(n)
        print(f"Цены: {prices}")

        # В зависимости от фильтра задаем ожидаемый порядок
        if filter_type == "Price: low to high":
            expected_prices = sorted(prices)
        elif filter_type == "Price: high to low":
            expected_prices = sorted(prices, reverse=True)

        # Проверка сортировки
        assert prices == expected_prices, f"Prices are not sorted correctly for filter - {filter_type}"

        # Закрываем браузер
        browser.close()
