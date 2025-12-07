import os
from models.config import Envs
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Browser
from pages.auth_page import LoginPage
from pages.spending_page import SpendingPage


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(frontend_url=os.getenv("FRONT_URL"),
                auth_url=os.getenv("AUTH_URL"),
                niffler_username=os.getenv('NIFFLER_USER'),
                niffler_password=os.getenv('NIFFLER_PASSWORD')
                )


@pytest.fixture
def login_page(page: Page, envs) -> LoginPage:
    return LoginPage(page, envs.auth_url)


@pytest.fixture(scope="session")
def setup_auth_state(browser: Browser, envs, tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("auth_data")
    state_path = temp_dir / "niffler_user.json"

    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page, envs.auth_url)
    login_page.open_login_page()
    login_page.login(envs.niffler_username, envs.niffler_password)
    login_page.spending_title_exists("History of Spendings")

    context.storage_state(path=str(state_path))
    context.close()

    yield state_path


@pytest.fixture(scope="function")
def page_with_auth(browser: Browser, setup_auth_state):
    context = browser.new_context(storage_state=str(setup_auth_state))
    page = context.new_page()

    yield page

    context.close()


@pytest.fixture(scope="function")
def spending_page(page_with_auth: Page, envs) -> SpendingPage:
    spending_page = SpendingPage(page_with_auth, envs.frontend_url)
    return spending_page
