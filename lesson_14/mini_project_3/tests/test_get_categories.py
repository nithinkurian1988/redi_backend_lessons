from fastapi import status
from fastapi.testclient import TestClient

from app.models import CategoryModel


def test_empty(test_client: TestClient):
    expected_response = []

    response = test_client.get("/categories/")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == expected_response


def test_get_categories(
    test_client: TestClient,
    groceries_category: CategoryModel,
):
    expected_response = [{"id": groceries_category.id, "name": groceries_category.name}]

    response = test_client.get("/categories/")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == expected_response
