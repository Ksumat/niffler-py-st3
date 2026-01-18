import allure
import pytest

from tools.assertions import assertion_is_equals, assertion_is_not_equals_in_list


@allure.feature("Траты")
@allure.title('Создание Траты')
@pytest.mark.parametrize("currency", ["KZT", "RUB", "EUR", "USD"])
def test_add_spend(spends_client, spend_data_for_add, currency,
                   delete_category_with_spendings):
    spend_data = {
        "amount": spend_data_for_add.amount,
        "description": spend_data_for_add.description,
        "category": spend_data_for_add.category,
        "spendDate": spend_data_for_add.spendDate,
        "currency": currency
    }

    spend = spends_client.add_spends(spend_data)
    assertion_is_equals(spend.amount, spend_data['amount'])
    assertion_is_equals(spend.description, spend_data['description'])
    assertion_is_equals(str(spend.spendDate)[:10], str(spend_data['spendDate'])[:10])
    assertion_is_equals(spend.currency, spend_data['currency'])
    assertion_is_equals(spend.category.name, spend_data['category'].name)


@allure.feature("Траты")
@allure.title('Создание траты  без описания')
def test_add_spend_without_description(spends_client, spend_data_for_add,
                                       delete_category_with_spendings):
    spend_data = {
        "amount": spend_data_for_add.amount,
        "description": "",
        "category": spend_data_for_add.category,
        "spendDate": spend_data_for_add.spendDate,
        "currency": spend_data_for_add.currency

    }

    spend = spends_client.add_spends(spend_data)
    assertion_is_equals(spend.amount, spend_data['amount'])
    assertion_is_equals(spend.description, spend_data['description'])
    assertion_is_equals(str(spend.spendDate)[:10], str(spend_data['spendDate'])[:10])
    assertion_is_equals(spend.currency, spend_data['currency'])
    assertion_is_equals(spend.category.name, spend_data['category'].name)


@allure.feature("Траты")
@allure.title('Редактирование траты')
def test_edit_spend(spends_client, spend_data_for_edit, add_spend,
                    delete_category_with_edited_spendings):
    spend_data = {
        "id": add_spend.id,
        "amount": spend_data_for_edit.amount,
        "description": spend_data_for_edit.description,
        "category": spend_data_for_edit.category,
        "spendDate": spend_data_for_edit.spendDate,
        "currency": spend_data_for_edit.currency

    }
    spend = spends_client.edit_spend(spend_data)
    assertion_is_equals(spend.amount, spend_data['amount'])
    assertion_is_equals(spend.description, spend_data['description'])
    assertion_is_equals(str(spend.spendDate)[:10], str(spend_data['spendDate'])[:10])
    assertion_is_equals(spend.currency, spend_data['currency'])
    assertion_is_equals(spend.category.name, spend_data['category'].name)


@allure.feature("Траты")
@allure.title('Удаление траты')
def test_delete_spend(spends_client, spend_data_for_edit, add_spend):
    spends_client.remove_spends(add_spend.id)
    spends = spends_client.get_spends()
    assertion_is_not_equals_in_list(add_spend.id, spends)


@allure.feature("Траты")
@allure.title('Получение траты')
def test_get_spend(spends_client, spend_data_for_edit, add_spend):
    spend = spends_client.get_spend(add_spend.id)
    assertion_is_not_equals_in_list(spend, add_spend)