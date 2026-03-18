import json
import os
from random import choice

from clients.oauth_client import OAuthClient
from database.userdata_db import UserdataDb
from models.config import Envs
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Browser

from models.enums import CategoryEnum
from models.spend import SpendAdd, SpendEdit
from pages.auth_page import LoginPage
from pages.profile_page import ProfilePage
from pages.spending_page import SpendingPage
from clients.spends_client import SpendsHttpClient
from database.spend_db import SpendDb

from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from pytest import FixtureDef, FixtureRequest
from tools.fakers import fake
from clients.kafka_client import KafkaClient


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(frontend_url=os.getenv("FRONT_URL"),
                auth_url=os.getenv("AUTH_URL"),
                niffler_username=os.getenv('NIFFLER_USER'),
                niffler_password=os.getenv('NIFFLER_PASSWORD'),
                gateway_url=os.getenv('GATEWAY_URL'),
                spend_db_url=os.getenv("SPEND_DB_URL"),
                kafka_address=os.getenv("KAFKA_ADDRESS"),
                userdata_db_url=os.getenv("USER_DB_URL")
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
def auth_token(envs: Envs):
    return OAuthClient(envs).get_token(envs.niffler_username, envs.niffler_password)


@pytest.fixture(scope="session")
def auth_client(envs: Envs) -> OAuthClient:
    return OAuthClient(envs)


@pytest.fixture(scope="function")
def spends_client(envs, auth_token) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth_token)


@pytest.fixture(scope="function")
def clean_spendings_setup(spends_client):
    spends_client.delete_all_spendings()
    yield
    spends_client.delete_all_spendings()


@pytest.fixture(params=[])
def category(request, spends_client, spend_db, clean_category_setup):
    category_name = request.param
    category = spends_client.add_category(name=category_name)
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


# @pytest.hookimpl(hookwrapper=True, trylast=True)
# def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
#     yield
#     logger = allure_logger(request.config)
#     item = logger.get_last_item()
#     scope_letter = fixturedef.scope[0].upper()
#     item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()


@pytest.fixture(scope="function")
def spend_data_for_add():
    return SpendAdd(
        amount=fake.float_amount(min_value=1.0, max_value=10000.0),
        description=fake.sentence()[:40],
        category={"name": fake.word().title()},
        currency=fake.currency(),
        spendDate=fake.past_datetime(days=1)
    )


@pytest.fixture
def delete_category_with_spendings(request, envs, spends_client, spend_data_for_add, spend_db):
    def teardown():
        spends = spends_client.get_spends()
        for spend in spends:
            if spend.category.name == spend_data_for_add.category.name:
                spends_client.remove_spends(ids=[spend.id])
        category_in_db = spend_db.get_category_by_name(envs.niffler_username, spend_data_for_add.category.name)
        spend_db.delete_category(category_in_db.id)

    request.addfinalizer(teardown)


@pytest.fixture
def delete_category_with_edited_spendings(request, envs, spends_client, spend_data_for_edit, spend_db):
    def teardown():
        spends = spends_client.get_spends()
        for spend in spends:
            if spend.category.name == spend_data_for_edit.category.name:
                spends_client.remove_spends(ids=[spend.id])
        category_in_db = spend_db.get_category_by_name(envs.niffler_username, spend_data_for_edit.category.name)
        spend_db.delete_category(category_in_db.id)

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def spend_data_for_edit():
    return SpendEdit(
        amount=fake.float_amount(min_value=1.0, max_value=10000.0),
        description=fake.sentence()[:40],
        category={"name": fake.word().title()},
        currency=fake.currency(),
        spendDate=fake.past_datetime(days=1)
    )


@pytest.fixture
def currency():
    currencies_list_symbols = ["₸", "₽", "€", "$"]
    return choice(currencies_list_symbols)


@pytest.fixture(scope="function")
def add_spend(spends_client, spend_data_for_add, currency, delete_category_with_spendings):
    spend_data = {
        "amount": spend_data_for_add.amount,
        "description": spend_data_for_add.description,
        "category": spend_data_for_add.category,
        "spendDate": spend_data_for_add.spendDate,
        "currency": spend_data_for_add.currency
    }
    spend = spends_client.add_spends(spend_data)
    return spend


@pytest.fixture
def category_value():
    return fake.word()


@pytest.fixture
def create_category(request, spends_client, spend_db, category_value):
    category = spends_client.add_category(name=category_value)

    def teardown():
        spend_db.delete_category(category.id)

    request.addfinalizer(teardown)
    return category


@pytest.fixture
def delete_category(request, envs, spend_db, category_value):
    def teardown():
        category_in_db = spend_db.get_category_by_name(envs.niffler_username, category_value)
        spend_db.delete_category(category_in_db.id)

    request.addfinalizer(teardown)


@pytest.fixture
def create_second_category(request, spends_client, spend_db):
    category = spends_client.add_category(name=CategoryEnum.CATEGORY)

    def teardown():
        spend_db.delete_category(category.id)

    request.addfinalizer(teardown)
    return category


@pytest.fixture(scope="session")
def kafka(envs: Envs):
    """Взаимодействие с Kafka"""
    with KafkaClient(envs) as k:
        yield k


@pytest.fixture(scope="session")
def user_db(envs: Envs) -> UserdataDb:
    return UserdataDb(envs)
