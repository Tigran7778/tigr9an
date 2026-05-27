import pytest
import logging
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from config_reader import ConfigReader

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config() -> ConfigReader:
    """Единственный экземпляр ConfigReader на всю сессию (Singleton)."""
    return ConfigReader()


@pytest.fixture(scope="session")
def browser_instance(config: ConfigReader):
    """
    Запускает браузер Chrome один раз на всю тестовую сессию.
    Закрывает браузер после завершения всех тестов.
    """
    headless: bool = config.get("browser", "headless", default=False)
    slow_mo: int   = config.get("browser", "slow_mo",  default=0)

    with sync_playwright() as pw:
        browser: Browser = pw.chromium.launch(
            channel="chrome",
            headless=headless,
            slow_mo=slow_mo,
        )
        logger.info(f"Browser launched (headless={headless}, slow_mo={slow_mo})")
        yield browser
        browser.close()
        logger.info("Browser closed")


@pytest.fixture(scope="function")
def context(browser_instance: Browser) -> BrowserContext:
    """
    Создаёт изолированный контекст браузера для каждого теста.
    Гарантирует независимость тестов (cookies / localStorage не текут).
    """
    ctx: BrowserContext = browser_instance.new_context()
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Открывает новую страницу (вкладку) в рамках контекста теста."""
    p: Page = context.new_page()
    yield p
    p.close()