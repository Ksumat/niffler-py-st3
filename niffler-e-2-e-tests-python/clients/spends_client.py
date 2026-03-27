import requests
from allure import step
from models.category import Category
from models.spend import Spend, SpendAdd, SpendEdit
from tools.sessions import BaseSession


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs, token: str):
        self.base_url = envs.gateway_url
        self.session = BaseSession(base_url=self.base_url)
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    @step("Отправить запрос на список категорий")
    def get_categories(self) -> list[Category]:
        response = self.session.get("/api/categories/all")
        return [Category.model_validate(item) for item in response.json()]

    @step("Отправить запрос на создание категории")
    def add_category(self, name) -> Category:
        response = self.session.post("/api/categories/add", json={
            "name": name
        })
        return Category.model_validate(response.json())

    @step("Отправить запрос на получение списка трат")
    def get_spend(self, spend_id: int) -> Spend:
        response = self.session.get(f"/api/spends/{spend_id}")
        return Spend.model_validate(response.json())

    @step("Отправить запрос на получение списка трат")
    def get_spends(self) -> list[Spend]:
        response = self.session.get("/api/spends/all")
        return [Spend.model_validate(item) for item in response.json()]

    @step("Отправить запрос на создание траты")
    def add_spends(self, spend: SpendAdd) -> Spend:
        spend_data = SpendAdd.model_validate(spend)
        response = self.session.post("/api/spends/add", json=spend_data.model_dump())
        return Spend.model_validate(response.json())

    @step("Отправить запрос на редактирование траты")
    def edit_spend(self, edit_spend: SpendEdit) -> Spend:
        spend_data = SpendEdit.model_validate(edit_spend)
        response = self.session.patch("/api/spends/edit", json=spend_data.model_dump())
        return Spend.model_validate(response.json())

    @step("Отправить запрос на удаление траты")
    def remove_spends(self, ids: list[str]):
        response = self.session.delete("/api/spends/remove", params={"ids": ids})
        return response

    @step("Отправить запрос на редактирование категории")
    def update_category(self, category):
        category_data = Category.model_validate(category)
        response = self.session.patch("/api/categories/update", json=category_data.model_dump())
        response.raise_for_status()
        return Category.model_validate(response.json())

    @step('Удаление всех трат API')
    def delete_all_spendings(self):
        all_spendings = self.get_spends()
        spending_ids = [spending.id for spending in all_spendings]
        if spending_ids:
            self.remove_spends(spending_ids)
