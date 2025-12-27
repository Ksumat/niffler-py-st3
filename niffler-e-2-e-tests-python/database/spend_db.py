import uuid
from typing import Sequence

from sqlalchemy import create_engine, Engine
from sqlmodel import Session, select

from models.spend import Category, Spend


class SpendDb:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_user_categories(self, username: str) -> Sequence[Category]:
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            return session.exec(statement).all()

    def add_user_category(self, username: str, category_name: str) -> Category:
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
        with Session(self.engine) as session:
            category = select(Category).where(
                Category.username == username,
                Category.name == category_name
            )
            return session.exec(category).first()

    def get_category_by_id(self, category_id: str) -> Category:
        with Session(self.engine) as session:
            category = select(Category).where(Category.id == category_id)
            return session.exec(category).first()

    def delete_category(self, category_id: str):
        with Session(self.engine) as session:
            category = session.get(Category, category_id)
            session.delete(category)
            session.commit()

    def get_spend_in_db(self, username: str):
        with Session(self.engine) as session:
            spend = select(Spend).where(Spend.username == username)
            result = session.exec(spend).all()
            return result