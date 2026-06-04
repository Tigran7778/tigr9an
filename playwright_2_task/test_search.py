import pytest
from playwright.sync_api import sync_playwright
from pages.main_page import MainPage
from pages.search_results_page import SearchResultsPage
from config_reader import ConfigReader


@pytest.fixture(scope="session")
def browser():
    config = ConfigReader()
    with sync_playwright() as p:
        # Можно выбрать браузер из конфигурации, если нужно
        browser_type = p.chromium  # или p.firefox, p.webkit
        browser = browser_type.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


def test_search_and_filter(page):
    config = ConfigReader()
    url = config.get("url")
    filters = config.get("filters", [])

    main_page = MainPage(page)
    main_page.open(url)

    # Выполняем поиск с именем из конфига
    main_page.search_article()

    search_results_page = SearchResultsPage(page)

    # Выбираем первый фильтр из списка
    if not filters:
        pytest.fail("Нет доступных фильтров в конфигурации")
    filter_info = filters[0]
    filter_type = filter_info["filter_type"]
    n = filter_info["city"]  # или "habits" — зависит от сценария

    # Применяем фильтр
    search_results_page.apply_filter(filter_type)

    # Получаем цены первых n статей
    prices = search_results_page.get_prices(n)

    # Проверка сортировки цен
    assert prices == sorted(prices), "Цены не отсортированы по возрастанию"

    print(f"Цены: {prices}")