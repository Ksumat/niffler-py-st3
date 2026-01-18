from marks import Pages, TestData
from tools.fakers import fake
import allure


@allure.feature('Траты')
class TestSpendPage:
    TEST_CATEGORY = "school"

    @allure.title('Оглавление страницы с тратами')
    @Pages.open_main_page
    def test_spending_title_statistic_exists(self, spending_page):
        spending_page.open_spending_page()
        spending_page.check_spending_page_titles('Statistics')

    @allure.title('Заведение новой траты')
    @Pages.open_main_page
    def test_create_new_spending(self, spending_page):
        amount = fake.integer()
        category = fake.word()
        description = fake.user_name()
        spending_page.open_spending_page()
        spending_page.create_spend(amount, category, description)
        spending_page.check_spending_exists(category, amount)

    @allure.title('Удаление траты')
    @Pages.open_main_page
    def test_delete_spending(self, spending_page):
        amount = fake.integer()
        category = fake.word()
        description = fake.user_name()
        spending_page.open_spending_page()
        spending_page.create_spend(amount, category, description)
        spending_page.delete_spend(category)
        spending_page.action_should_have_signal_text("Spendings succesfully delete")

    @allure.title('Удаление всех трат')
    @Pages.open_spending_page
    @TestData.category(TEST_CATEGORY)
    @TestData.spends({
        "amount": "108.51",
        "description": "QA.GURU Python Advanced 1",
        "category": {
            "name": TEST_CATEGORY
        },
        "spendDate": "2024-08-08T18:39:27.955Z",
        "currency": "RUB"
    })
    def test_delete_all_spending(self, spending_page, category):
        spending_page.check_delete_spending("Spendings succesfully deleted")

    @allure.title('Изменение валюты в трате')
    @Pages.open_spending_page
    @TestData.category(TEST_CATEGORY)
    @TestData.spends({
        "amount": "108.51",
        "description": "QA.GURU Python Advanced 1",
        "category": {
            "name": TEST_CATEGORY
        },
        "spendDate": "2024-08-08T18:39:27.955Z",
        "currency": "RUB"
    })
    def test_edit_spending_currency_usd(self, spending_page, category):
        spending_page.edit_spending_currency("USD")
        spending_page.action_should_have_signal_text("Spending is edited successfully")

    @allure.title('Добавление новой траты, проверка в бд')
    @Pages.open_spending_page
    @TestData.category(TEST_CATEGORY)
    @TestData.spends({
        "amount": 101.1,
        "description": "test_description",
        "category": {
            "name": TEST_CATEGORY
        },
        "spendDate": "2025-08-08T18:39:27.955Z",
        "currency": "RUB"
    })
    def test_add_new_spending(self, envs, spending_page, spend_db, spends, category):
        added_spend_in_db = spend_db.get_spend_in_db(envs.niffler_username)

        assert added_spend_in_db[0].amount == spends.amount
        assert added_spend_in_db[0].description == spends.description
        assert added_spend_in_db[0].currency == spends.currency

        spending_page.check_spending_exists(self.TEST_CATEGORY, spends.amount)
