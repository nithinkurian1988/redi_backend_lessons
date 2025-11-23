from unittest.mock import ANY
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.constants import Currencies
from app.models import CategoryModel, TransactionModel


def test_missing_spending_category_name(test_client: TestClient):
    response = test_client.post("/transactions/")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT, response.text


def test_category_not_found(test_client: TestClient):
    payload = {
        "category_id": 123,
        "amount": 100,
        "currency": Currencies.EURO,
    }

    response = test_client.post("/transactions/", json=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_create_transaction(
    session: Session,
    test_client: TestClient,
    groceries_category: CategoryModel,
):
    payload = {
        "category_id": groceries_category.id,
        "amount": 100,
        "currency": Currencies.EURO,
    }
    expected_response = {"id": ANY, **payload}

    response = test_client.post("/transactions/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert (data := response.json()) == expected_response
    assert (
        transaction := session.execute(select(TransactionModel).filter(TransactionModel.id == data["id"])).scalar()
    ) is not None
    assert transaction.category_id == payload["category_id"]
    assert transaction.amount == payload["amount"]
    assert transaction.currency.value == payload["currency"]
