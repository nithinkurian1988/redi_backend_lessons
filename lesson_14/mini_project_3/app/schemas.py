from pydantic import BaseModel, ConfigDict

from app.constants import Currencies


# Category schemas


class CreateCategory(BaseModel):
    name: str


class Category(CreateCategory):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Transaction schemas


class CreateTransaction(BaseModel):
    category_id: int
    amount: int
    currency: Currencies


class Transaction(CreateTransaction):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Transaction search parameters schema

class TransactionSearchParams(BaseModel):
    category_id: int | None = None
    min_amount: float | None = None
    max_amount: float | None = None
    currency: Currencies | None = None

# Summary schemas


class TransactionSummary(BaseModel):
    currency: Currencies
    total: int


class CategorySummary(BaseModel):
    id: int
    currencies: list[TransactionSummary]
