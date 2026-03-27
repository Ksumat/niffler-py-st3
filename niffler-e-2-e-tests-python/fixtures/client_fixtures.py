import pytest
from models.enums import CategoryEnum
from models.spend import SpendAdd, SpendEdit
from clients.spends_client import SpendsHttpClient
from database.spend_db import SpendDb
from random import choice
from tools.fakers import fake


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
