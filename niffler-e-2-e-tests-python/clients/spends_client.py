import requests
from urllib.parse import urljoin
from models.spend import Category, Spend, SpendAdd, CategoryAdd


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })

    def get_categories(self) -> list[CategoryAdd]:
        response = self.session.get(urljoin(self.base_url, '/api/categories/all'))
        response.raise_for_status()
        return [CategoryAdd.model_validate(item) for item in response.json()]

    def add_category(self, category: CategoryAdd) -> Category:
        category = CategoryAdd.model_validate(category)
        response = self.session.post(urljoin(self.base_url, '/api/categories/add'), json=category.model_dump())
        response.raise_for_status()
        return Category.model_validate(response.json())

    def remove_category(self, ids: list[str]):
        url = urljoin(self.base_url, "/api/categories/remove")
        response = self.session.delete(url, params={"ids": ids})
        response.raise_for_status()

    def get_spends(self) -> list[Spend]:
        response = self.session.get(urljoin(self.base_url, '/api/v2/spends/all'))
        response.raise_for_status()
        return [Spend.model_validate(item) for item in response.json()["content"]]

    def add_spends(self, spend: dict) -> Spend:
        url = urljoin(self.base_url, "/api/spends/add")
        spend_data = SpendAdd.model_validate(spend)
        response = self.session.post(url, json=spend_data.model_dump())
        response.raise_for_status()
        return Spend.model_validate(response.json())

    def remove_spends(self, ids: list[str]):
        ids_param = ",".join(ids)
        url = urljoin(self.base_url, "/api/spends/remove")
        response = self.session.delete(url, params={"ids": ids_param})
        response.raise_for_status()

    def delete_all_spendings(self):
        all_spendings = self.get_spends()
        spending_ids = [spending.id for spending in all_spendings]
        if spending_ids:
            self.remove_spends(spending_ids)
