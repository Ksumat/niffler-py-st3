from marks import Pages, TestData
from tools.fakers import fake
import allure

TEST_CATEGORY = "school"


@allure.feature('Категории')
class TestCategories:
    TEST_CATEGORY_BD = "db_category"

    @allure.title('Создание новой категории')
    @Pages.open_profile_page
    def test_create_category(self, profile_page):
        new_category = fake.word()
        profile_page.add_category(new_category)
        profile_page.successful_adding(new_category)

    @allure.title('Создание новой категории с пустым названием')
    @Pages.open_profile_page
    def test_add_empty_name_category(self, profile_page):
        profile_page.adding_empty_name_category()
        profile_page.check_error_message("Error while adding category : Category can not be blank")

    @allure.title('Создание новой категории с существующим названием')
    @Pages.open_profile_page
    @TestData.category(TEST_CATEGORY)
    def test_add_same_category(self, category, profile_page):
        same_category = category
        profile_page.add_category(same_category)
        profile_page.check_error_message(f"Error while adding category {same_category}: Cannot save duplicates")

    @allure.title('Редактирование названия категории')
    @Pages.open_profile_page
    def test_edit_category_name(self, profile_page):
        profile_page.add_new_category_if_empty()

        old_name = profile_page.category_name.first.text_content()
        new_name = fake.word()
        profile_page.edit_first_category_name(new_name)
        profile_page.check_category_name(new_name, old_name)

    @allure.title('Добавление категории и проверка в БД')
    @TestData.category(TEST_CATEGORY_BD)
    def test_add_category_and_check_db(self, envs, category, spend_db):
        user_categories = spend_db.get_user_categories(envs.niffler_username)
        user_category_names = [category.name for category in user_categories]

        assert len(user_categories) > 0, "Категорий у этого пользовтаеля нет"
        assert category in user_category_names

    @allure.title('Удаление категории и проверка в БД')
    def test_delete_category_and_check_db(self, envs, spend_db):
        new_category = spend_db.add_user_category(envs.niffler_username, self.TEST_CATEGORY_BD)

        search_before_delete = spend_db.get_category_by_id(new_category.id)
        assert search_before_delete.name == self.TEST_CATEGORY_BD

        spend_db.delete_category(new_category.id)

        search_after_delete = spend_db.get_category_by_name(envs.niffler_username, new_category.name)
        assert search_after_delete is None


@allure.feature('Информация пользователя')
class TestProfileInfo:

    @allure.title('Оглавление страницы информации о пользователе')
    @Pages.open_profile_page
    def test_profile_title(self, profile_page):
        profile_page.check_profile_title('Profile')

    @allure.title('Добавление имени пользователя')
    @Pages.open_profile_page
    def test_create_user_name(self, profile_page):
        user_name = fake.user_name()
        profile_page.add_user_name(user_name)
        profile_page.check_successful_adding_name(user_name)

    @allure.title('Удаление имени пользователя')
    @Pages.open_profile_page
    def test_delete_profile_name(self, profile_page):
        profile_page.add_profile_name_if_empty()
        profile_page.add_user_name("")
        profile_page.check_successful_adding_name("")
