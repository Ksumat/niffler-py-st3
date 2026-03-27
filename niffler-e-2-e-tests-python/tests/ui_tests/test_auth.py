import allure
from marks import Pages
from tools.fakers import fake


@allure.feature('Авторизации и аутентификация')
class TestAuthPage:

    @allure.title('Регистрация нового пользователя в системе')
    @Pages.open_login_page
    def test_registration_new_user(self, login_page):
        login_page.registration_user(fake.user_name(), fake.password())
        login_page.text_should_be_visible("Congratulations! You've registered!")

    @allure.title('Регистрация существующего пользователя в системе')
    @Pages.open_login_page
    def test_registration_existed_user(self, login_page, envs):
        login_page.registration_user(envs.niffler_username, envs.niffler_password)
        login_page.text_unsuccessful_registration(f'Username `{envs.niffler_username}` already exists')

    @allure.title('Авторизация пользователя в системе')
    @Pages.open_login_page
    def test_login_user(self, login_page, envs):
        login_page.login(envs.niffler_username, envs.niffler_password)
        login_page.spending_title_exists("History of Spendings")

    @allure.title('Переход на страницу регистрации')
    @Pages.open_login_page
    def test_navigate_from_authorization_to_registration(self, login_page):
        login_page.open_registration_page()
        login_page.register_form_should_have_title('Sign up')

    @allure.title('Авторизация с невалидным логином и паролем')
    @Pages.open_login_page
    def test_login_user_with_invalid_login_or_password(self, login_page):
        login_page.login("username", "password")
        login_page.text_unsuccessful_login('Bad credentials')

    @allure.title('Регистрация пользователя с невалидным именем')
    @Pages.open_login_page
    def test_registration_new_user_with_forbidden_name(self, login_page):
        login_page.registration_user('ws', fake.password())
        login_page.text_unsuccessful_registration("Allowed username length should be from 3 to 50 characters")

    @allure.title('Регистрация пользователя с невалидным паролем')
    @Pages.open_login_page
    def test_registration_new_user_with_forbidden_pass(self, login_page):
        login_page.registration_user(fake.user_name(), 'ws')
        login_page.text_unsuccessful_registration_pass_error("Allowed password length should be from 3 to 12 characters")
