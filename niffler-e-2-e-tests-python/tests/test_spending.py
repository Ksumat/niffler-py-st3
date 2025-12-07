from tools.fakers import fake


class TestSpendPage:

    def test_spending_title_statistic_exists(self, spending_page):
        spending_page.open_spending_page()
        spending_page.check_spending_page_titles('Statistics')

    def test_create_new_spending(self, spending_page):
        amount = fake.integer()
        category = fake.word()
        description = fake.user_name()
        spending_page.open_spending_page()
        spending_page.create_spend(amount, category, description)
        spending_page.check_spending_exists(category, amount)

    def test_delete_spending(self, spending_page):
        amount = fake.integer()
        category = fake.word()
        description = fake.user_name()
        spending_page.open_spending_page()
        spending_page.create_spend(amount, category, description)
        spending_page.delete_spend(category)
        spending_page.action_should_have_signal_text("Spendings succesfully delete")