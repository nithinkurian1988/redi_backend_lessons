from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.constants import Currencies


class DbModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class CategoryModel(DbModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(length=25), nullable=False, unique=True)


class TransactionModel(DbModel):
    __tablename__ = "transactions"

    category_id: Mapped[str] = mapped_column(ForeignKey(CategoryModel.id), nullable=False)
    amount: Mapped[int]
    currency: Mapped[Currencies]
