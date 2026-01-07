import json
import os
from models.config import Envs
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Browser, sync_playwright

from models.spend import CategoryAdd
from pages.auth_page import LoginPage
from pages.profile_page import ProfilePage
from pages.spending_page import SpendingPage
from clients.spends_client import SpendsHttpClient
from database.spend_db import SpendDb

import allure
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener
from pytest import Item, FixtureDef, FixtureRequest


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(frontend_url=os.getenv("FRONT_URL"),
                auth_url=os.getenv("AUTH_URL"),
                niffler_username=os.getenv('NIFFLER_USER'),
                niffler_password=os.getenv('NIFFLER_PASSWORD'),
                gateway_url=os.getenv('GATEWAY_URL'),
                spend_db_url=os.getenv("SPEND_DB_URL")
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


@pytest.fixture(scope="function")
def clean_spendings_setup(spends_client):
    spends_client.delete_all_spendings()
    yield
    spends_client.delete_all_spendings()


@pytest.fixture(params=[])
def category(request, spends_client, spend_db, clean_category_setup):
    category_name = request.param
    category = spends_client.add_category(CategoryAdd(name=category_name))
    yield category.name
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(request, spends_client, clean_spendings_setup, category):
    spend = spends_client.add_spends(request.param)
    yield spend
    all_spends = spends_client.get_spends()
    if spend.id in [s.id for s in all_spends]:
        spends_client.remove_spends([spend.id])


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


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture(scope="function")
def clean_category_setup(spend_db, envs):
    all_categories = spend_db.get_user_categories(envs.niffler_username)
    for category in all_categories:
        spend_db.delete_category(category.id)
    yield
    all_categories = spend_db.get_user_categories(envs.niffler_username)
    for category in all_categories:
        spend_db.delete_category(category.id)


def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()
