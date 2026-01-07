from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    PATH = '/login'

    def __init__(self, page: Page, base_url):
        super().__init__(page)
        self.base_url = base_url + self.PATH
        self.spending_title = page.locator('[id="spendings"]')
        self.spending_bottom_title = page.locator('[class="MuiBox-root css-11i3wq6"]')
        self.register_form = page.locator('[class="form__register"]')
        self.username = page.locator('input[name=username]')
        self.password = page.locator('input[name=password]')
        self.submit_password_field = page.locator('input[name=passwordSubmit]')
        self.submit_button = page.locator('button[type=submit]')
        self.successful_registration = page.locator('.form__paragraph')
        self.unsuccessful_registration = page.locator('.form__error')
        self.unsuccessful_registration_pass = page.locator('#passwordBtn + .form__error')
        self.register_form_title = page.locator('[id="register-form"]')
        self.login_warning = page.locator("form[action='/login'] p")

    def open_login_page(self) -> None:
        with allure.step('Открытие страницы логина'):
            self.goto(self.base_url)

    def login(self, username: str, password: str) -> None:
        with allure.step('Авторизация'):
            self.username.fill(username)
            self.password.fill(password)
            self.submit_button.click()

    def open_registration_page(self) -> None:
        with allure.step('Открытие страницы регистрации'):
            self.register_form.click()

    def spending_title_exists(self, title: str) -> None:
        with allure.step('Проверка оглавления страницы трат'):
            expect(self.spending_title).to_contain_text(title)

    def registration_user(self, username: str, password: str) -> None:
        with allure.step('Регистрация пользователя'):
            self.register_form.click()
            self.username.fill(username)
            self.password.fill(password)
            self.submit_password_field.fill(password)
            self.submit_button.click()

    def register_form_should_have_title(self, title: str) -> None:
        with allure.step('Проверка, что на форме регистрации есть текст'):
            expect(self.register_form_title).to_contain_text(title)

    def text_should_be_visible(self, text: str) -> None:
        with allure.step('Проверка, текста при регистрации'):
            expect(self.successful_registration).to_contain_text(text)

    def text_unsuccessful_registration(self, text: str) -> None:
        with allure.step('Проверка, текста при неудачной регистрации'):
            expect(self.unsuccessful_registration).to_contain_text(text)

    def text_unsuccessful_registration_pass_error(self, text: str) -> None:
        with allure.step('Проверка, текста при регистрации с невалидным паролем'):
            expect(self.unsuccessful_registration_pass).to_contain_text(text)

    def text_unsuccessful_login(self, text: str) -> None:
        with allure.step('Проверка, текста при неудачной авторизации'):
            expect(self.login_warning).to_contain_text(text)
