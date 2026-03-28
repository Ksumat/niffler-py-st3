import pytest
import json
from models.config import Envs
from pages.auth_page import LoginPage
from playwright.sync_api import Browser
from clients.oauth_client import OAuthClient


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
