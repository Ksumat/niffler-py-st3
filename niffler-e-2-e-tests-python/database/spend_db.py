import uuid
from typing import Sequence

from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select

from models.spend import Category, Spend
import allure
from allure_commons.types import AttachmentType


class SpendDb:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

    def get_user_categories(self, username: str) -> Sequence[Category]:
        with allure.step('Получение категорий пользователя БД'):
            with Session(self.engine) as session:
                statement = select(Category).where(Category.username == username)
                return session.exec(statement).all()

    def add_user_category(self, username: str, category_name: str) -> Category:
        with allure.step('Добавление категории БД'):
            with Session(self.engine) as session:
                new_category = Category(
                    id=str(uuid.uuid4()),
                    name=category_name,
                    username=username
                )

                session.add(new_category)
                session.commit()
                session.refresh(new_category)

                return new_category

    def get_category_by_name(self, username: str, category_name: str) -> Category:
        with allure.step('Получение категории по названию БД'):
            with Session(self.engine) as session:
                category = select(Category).where(
                    Category.username == username,
                    Category.name == category_name
                )
                return session.exec(category).first()

    def get_category_by_id(self, category_id: str) -> Category:
        with allure.step('Получение категории по айди БД'):
            with Session(self.engine) as session:
                category = select(Category).where(Category.id == category_id)
                return session.exec(category).first()

    def delete_category(self, category_id: str):
        with allure.step('Удаление категории БД'):
            with Session(self.engine) as session:
                category = session.get(Category, category_id)
                session.delete(category)
                session.commit()

    def get_spend_in_db(self, username: str):
        with allure.step('Получения списка трат БД'):
            with Session(self.engine) as session:
                spend = select(Spend).where(Spend.username == username)
                result = session.exec(spend).all()
                return result