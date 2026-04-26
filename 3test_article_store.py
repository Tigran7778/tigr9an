from playwright.sync_api import Page
from faker import Faker

fake = Faker()
MY_URL = 'http://144.31.139.115:5000/'


def test_login_page_title(page: Page):
    # Генерируем случайные данные
    username = fake.user_name()
    password = fake.password()

    # Переходим на главную страницу
    page.goto(MY_URL)

    # Нажимаем на ссылку для перехода к форме входа
    page.locator('//a[contains(@data-testid, "login")]').click()

    # Проверка заголовка страницы
    expected_title = 'Login'
    actual_title = page.title()
    assert actual_title == expected_title, (
        f"Ошибка заголовка: ожидали '{expected_title}', получили '{actual_title}'"
    )

    # Вводим данные
    page.locator('//input[contains(@data-testid, "login-username")]').fill(username)
    page.locator('//input[contains(@data-testid, "login-password")]').fill(password)

    # Нажимаем кнопку для входа
    page.locator('//button[contains(@data-testid, "login-submit")]').click()

    # Ждём появления сообщения об ошибке
    error_xpath = '//div[contains(@data-testid, "login-error-inline") and normalize-space()]'
    error_locator = page.locator(error_xpath)

    # Ждем, пока элемент станет видимым и в нем появится текст
    error_locator.wait_for(state='visible', timeout=10000)

    # Вычитываем актуальный текст ошибки
    actual_error_text = error_locator.inner_text().strip()

    # Ожидаемый текст ошибки
    expected_error_text = "Invalid login or password."

    # Проверка с подробным выводом в случае падения.
    assert expected_error_text in actual_error_text, (
        f"\n\n[ПРОВЕРКА ТЕКСТА ОШИБКИ ПРОВАЛЕНА]"
        f"\nВведенный логин: {username}"
        f"\nВведенный пароль: {password}"
        f"\nОжидалось вхождение: '{expected_error_text}'"
        f"\nФактически на экране: '{actual_error_text}'\n"
    )
