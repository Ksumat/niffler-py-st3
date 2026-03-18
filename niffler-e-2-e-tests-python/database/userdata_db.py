from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select
from models.config import Envs
from models.user import User
from tools.allure_helpers import attach_sql


class UserdataDb:
    """Клиент для взаимодействия с БД пользователей"""

    engine: Engine

    def __init__(self, envs: Envs):
        self.engine = create_engine(envs.userdata_db_url)
        event.listen(self.engine, "do_execute", fn=attach_sql)

    def get_user_by_username(self, username: str) -> User:
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            return session.exec(statement).first()

