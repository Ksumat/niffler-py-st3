from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from models.category import Category, CategoryAdd


class SpendBd(SQLModel, table=True):
    __tablename__ = "spend"
    id: str = Field(default=None, primary_key=True)
    username: str
    amount: float
    description: str
    currency: str


class Spend(BaseModel):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: Category
    spendDate: datetime
    currency: str
    username: str


class SpendAdd(BaseModel):
    amount: float
    description: str
    category: CategoryAdd
    spendDate: str
    currency: str


class SpendEdit(BaseModel):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: CategoryAdd
    spendDate: str
    currency: str
