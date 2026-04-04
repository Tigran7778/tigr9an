from playwright.sync_api import Page, expect

def test_login_page_title(page: Page):
    page.goto('http://144.31.139.115:5000/')
    page.locator('xpath=//a[contains(@class, "login")]').click()
    expect(page).to_have_title('Login')
    page.locator('//*[@id="username"]').fill('dssdfer')
    page.locator('//*[@id="password"]').fill('we43324rrfsd')
    page.keyboard.press('Enter')
    expect(page.locator("//div[contains(@class, 'login-error')]")).to_have_text("Invalid login or password.")