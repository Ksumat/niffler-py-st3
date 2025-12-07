from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class SpendingPage(BasePage):
    def __init__(self, page: Page, base_url):
        super().__init__(page)
        self.base_url = base_url
        self.statistic_title = page.locator('[id="stat"] h2')
        self.new_spend_button = page.locator('[href="/spending"]')
        self.title_new_spending_list = page.locator('.MuiTypography-root.MuiTypography-h5.css-w1t7b3')
        self.amount = page.locator('#amount')
        self.category = page.locator('#category')
        self.description = page.locator('#description')
        self.button_add_spending = page.locator('#save')
        self.category_name = lambda name_category: page.locator('#spendings tbody', has_text=f"{name_category}")
        self.delete_button = page.locator('#delete')
        self.delete_button_approve = page.locator("//div[@role='dialog']//button[contains(text(), 'Delete')]")
        self.spending = page.locator('#spendings')
        self.spending_table_cells = page.locator('.table.spendings-table td')

    def open_spending_page(self) -> None:
        self.goto(self.base_url)

    def check_spending_page_titles(self, text: str):
        expect(self.statistic_title).to_contain_text(text)

    def create_spend(self, amount: int, test_category: str, description: str) -> None:
        self.new_spend_button.click()
        expect(self.title_new_spending_list).to_contain_text('Add new spending')
        self.amount.fill(str(amount))
        self.category.fill(f'{test_category}')
        self.description.fill(f'{description}')
        self.button_add_spending.click()

    def check_spending_exists(self, category: str, amount: str):
        expected_text = f"{category} {amount}"
        cells = self.spending_table_cells
        count = cells.count()
        for i in range(count):
            cell_text = cells.nth(i).text_content().strip()
            if expected_text in cell_text:
                print(f"Найдена ячейка с текстом: {cell_text}")

    def delete_spend(self, name_category: str) -> None:
        self.category_name(name_category).click()
        self.delete_button.click()
        self.delete_button_approve.click()

    def action_should_have_signal_text(self, text: str) -> None:
        expect(self.page.get_by_text(text)).to_be_visible()
