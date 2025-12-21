import json
import os
from models.config import Envs
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Browser, sync_playwright
from pages.auth_page import LoginPage
from pages.profile_page import ProfilePage
from pages.spending_page import SpendingPage
from clients.spends_client import SpendsHttpClient


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(frontend_url=os.getenv("FRONT_URL"),
                auth_url=os.getenv("AUTH_URL"),
                niffler_username=os.getenv('NIFFLER_USER'),
                niffler_password=os.getenv('NIFFLER_PASSWORD'),
                gateway_url=os.getenv('GATEWAY_URL')
                )


# @pytest.fixture(scope="session")
# def browser() -> Browser:
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=1000)  # для удобства отладки
#         yield browser
#         browser.close()


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


@pytest.fixture(scope="function")
def profile_page(page_with_auth: Page, envs) -> ProfilePage:
    profile_page = ProfilePage(page_with_auth, envs.frontend_url)
    return profile_page


@pytest.fixture(scope="session")
def get_token_from_user_state(setup_auth_state):
    with open(setup_auth_state) as json_file:
        data = json.load(json_file)
        api_token = data['origins'][0]['localStorage'][3]['value']
    return api_token


@pytest.fixture(scope="session")
def spends_client(get_token_from_user_state, envs) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, get_token_from_user_state)


@pytest.fixture(params=[])
def category(request, spends_client):
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_names = [category["name"] for category in current_categories]
    if category_name not in category_names:
        spends_client.add_category(category_name)
    return category_name


@pytest.fixture(params=[])
def spends(request, spends_client: SpendsHttpClient):
    spend = spends_client.add_spends(request.param)
    yield spend
    all_spends = spends_client.get_spends()
    if spend["id"] in [spend["id"] for spend in all_spends]:
        spends_client.remove_spends([spend["id"]])


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
