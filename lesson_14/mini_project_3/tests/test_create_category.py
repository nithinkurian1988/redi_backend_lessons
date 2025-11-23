from unittest.mock import ANY
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CategoryModel


def test_missing_spending_category_name(test_client: TestClient):
    response = test_client.post("/categories/")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT, response.text


def test_already_created_category_name(
    test_client: TestClient,
    groceries_category: CategoryModel,
):
    payload = {"name": groceries_category.name}

    response = test_client.post("/categories/", json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT, response.text


def test_create_category(test_client: TestClient, session: Session):
    payload = {"name": "new-category"}
    expected_response = {"id": ANY, **payload}

    response = test_client.post("/categories/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert (data := response.json()) == expected_response
    assert (
        category := session.execute(select(CategoryModel).filter(CategoryModel.id == data["id"])).scalar()
    ) is not None
    assert category.name == payload["name"]
