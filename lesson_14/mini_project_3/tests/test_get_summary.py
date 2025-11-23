from fastapi import status
from fastapi.testclient import TestClient

from app.models import CategoryModel, TransactionModel


def test_empty_categories(test_client: TestClient):
    expected_response = []

    response = test_client.get("/summary/")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == expected_response


def test_one_empty_category(
    test_client: TestClient,
    groceries_category: CategoryModel,
):
    expected_response = []

    response = test_client.get("/summary/")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == expected_response


def test_one_category_multiple_transactions(
    test_client: TestClient,
    groceries_category: CategoryModel,
    groceries_first_euro_transaction: TransactionModel,
    groceries_second_euro_transaction: TransactionModel,
):
    expected_response = [
        {
            "id": groceries_category.id,
            "currencies": [
                {
                    "currency": groceries_first_euro_transaction.currency.value,
                    "total": (groceries_first_euro_transaction.amount + groceries_second_euro_transaction.amount),
                }
            ],
        },
    ]

    response = test_client.get("/summary/")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == expected_response


def test_multiple_categories_multiple_transactions(
    test_client: TestClient,
    groceries_category: CategoryModel,
    groceries_first_euro_transaction: TransactionModel,
    groceries_second_euro_transaction: TransactionModel,
    entertainment_category: CategoryModel,
    entertainment_first_lira_transaction: TransactionModel,
    entertainment_first_rouble_transaction: TransactionModel,
):
    expected_response = [
        {
            "id": groceries_category.id,
            "currencies": [
                {
                    "currency": groceries_first_euro_transaction.currency.value,
                    "total": (groceries_first_euro_transaction.amount + groceries_second_euro_transaction.amount),
                }
            ],
        },
        {
            "id": entertainment_category.id,
            "currencies": [
                {
                    "currency": entertainment_first_lira_transaction.currency.value,
                    "total": entertainment_first_lira_transaction.amount,
                },
                {
                    "currency": entertainment_first_rouble_transaction.currency.value,
                    "total": entertainment_first_rouble_transaction.amount,
                },
            ],
        },
    ]

    response = test_client.get("/summary/")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == expected_response
