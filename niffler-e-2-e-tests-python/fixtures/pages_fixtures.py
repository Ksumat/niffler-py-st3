import pytest
from pages.profile_page import ProfilePage
from pages.spending_page import SpendingPage
from pages.auth_page import LoginPage
from playwright.sync_api import Page


@pytest.fixture
def login_page(page: Page, envs) -> LoginPage:
    return LoginPage(page, envs.auth_url)


@pytest.fixture(scope="function")
def spending_page(page_with_auth: Page, envs) -> SpendingPage:
    spending_page = SpendingPage(page_with_auth, envs.frontend_url)
    return spending_page


@pytest.fixture(scope="function")
def profile_page(page_with_auth: Page, envs) -> ProfilePage:
    profile_page = ProfilePage(page_with_auth, envs.frontend_url)
    return profile_page


@pytest.fixture()
def open_main_page(spending_page):
    spending_page.open_spending_page()


@pytest.fixture()
def open_spending_page(spending_page, spends):
    spending_page.open_spending_page()


@pytest.fixture()
def open_login_page(login_page):
    login_page.open_login_page()


@pytest.fixture()
def open_profile_page(profile_page):
    profile_page.open_profile_page()
