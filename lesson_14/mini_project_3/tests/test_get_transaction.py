from fastapi import status
from fastapi.testclient import TestClient

from app.models import TransactionModel


def test_not_found(test_client: TestClient):
    response = test_client.get("/transactions/123")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_get_transaction(
    test_client: TestClient,
    groceries_first_euro_transaction: TransactionModel,
):
    url = f"/transactions/{groceries_first_euro_transaction.id}"

    response = test_client.get(url)

    assert response.status_code == status.HTTP_200_OK, response.text
