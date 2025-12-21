from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from tools.fakers import fake


class ProfilePage(BasePage):
    PATH = '/profile'

    def __init__(self, page: Page, base_url):
        super().__init__(page)
        self.base_url = base_url + self.PATH
        self.input_category = page.locator('#category')
        self.alert = page.locator('div[role="alert"] div:nth-child(2)')
        self.error_alert = page.locator('.add-category__input-container button')
        self.name = page.locator('#name')
        self.submit_button = page.locator('[type="submit"]')
        self.profile_title = page.locator('.MuiTypography-root.MuiTypography-h5.css-w1t7b3')
        self.edit_category_name = page.locator("[aria-label='Edit category']")
        self.category_name = page.locator("[class*='css-14vsv3w']")
        self.edit_category_input = page.locator("[placeholder='Edit category']")

    def open_profile_page(self) -> None:
        self.goto(self.base_url)

    def add_category(self, category):
        self.input_category.fill(category)
        self.input_category.press('Enter')

    def successful_adding(self, category: str):
        expect(self.alert).to_contain_text(f"You've added new category: {category}")

    def check_error_message(self, message: str):
        expect(self.alert).to_contain_text(message)

    def adding_empty_name_category(self):
        self.input_category.fill('  ')
        self.input_category.press('Enter')

    def add_user_name(self, name: str):
        self.name.clear()
        self.name.fill(name)
        self.submit_button.click()

    def check_successful_adding_name(self, name):
        expect(self.alert).to_contain_text(f"Profile successfully updated")
        expect(self.name).to_have_value(f"{name}")

    def check_profile_title(self, title: str):
        expect(self.profile_title).to_contain_text(title)

    def add_profile_name_if_empty(self):
        name = "test_name"
        if self.name.text_content() != name:
            self.add_user_name(name)

    def add_new_category_if_empty(self):
        category_name = fake.word()
        if self.edit_category_name.first.is_hidden():
            self.add_category(category_name)

    def edit_first_category_name(self, name: str):
        self.edit_category_name.first.click()
        self.edit_category_input.fill(name)
        self.page.keyboard.press("Enter")

    def check_category_name(self, new_name, old_name):
        expect(self.category_name.first).to_have_text(new_name)
        self.edit_first_category_name(old_name)
        expect(self.category_name.first).to_have_text(old_name)