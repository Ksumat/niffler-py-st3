from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class UserName(BaseModel):
    username: str


class User(SQLModel, table=True):
    """Модель для таблицы в БД с пользователями"""
    __tablename__ = "user"
    id: str = Field(default=None, primary_key=True)
    username: str
    currency: str = Field(default="RUB")
    firstname: str | None = None
    surname: str | None = None
    photo: bytes | None = None
    photo_small: bytes | None = None
    full_name: str | None = None
