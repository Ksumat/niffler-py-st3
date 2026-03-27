import allure
import pytest

from models.category import Category
from models.enums import CategoryEnum
from tools.assertions import assertion_is_equals, assertion_in


@allure.feature("Категории")
class TestCategories:

    @allure.title('Создание категории')
    @pytest.mark.usefixtures("delete_category")
    def test_add_new_category(self, spends_client, category_value, envs):
        category = spends_client.add_category(category_value)
        assertion_is_equals(category.name, category_value)
        assertion_is_equals(category.username, envs.niffler_username)
        assertion_is_equals(category.archived, False)

    @allure.title('Редактирование категории')
    @pytest.mark.parametrize("archived", [False, True])
    def test_edit_category(self, spends_client, create_category, archived):
        category_data = Category(
            id=create_category.id,
            username=create_category.username,
            name=CategoryEnum.CATEGORY_EDIT,
            archived=archived
        )
        category = spends_client.update_category(category_data)
        assertion_is_equals(category.name, CategoryEnum.CATEGORY_EDIT)
        assertion_is_equals(category.username, category_data.username)
        assertion_is_equals(category.archived, category_data.archived)

    @allure.title('Получить все категории')
    def test_get_all_categories(self, spends_client, create_category, create_second_category):
        categories = spends_client.get_categories()
        assertion_in(create_category, categories)
        assertion_in(create_second_category, categories)
