from locale import currency
import string
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.injections import get_category_repository, get_transaction_repository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas import Transaction, CreateTransaction, TransactionSearchParams


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {}},
)
def create_transaction(
    transaction_to_create: CreateTransaction,
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)],
    transaction_repository: Annotated[TransactionRepository, Depends(get_transaction_repository)],
) -> Transaction:
    try:
        return transaction_repository.create_transaction(transaction_to_create=transaction_to_create)
    except transaction_repository.CategoryNotFound as exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exception


@router.get(
    "/{transaction_id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def get_transaction(
    transaction_id: int,
    transaction_repository: Annotated[TransactionRepository, Depends(get_transaction_repository)],
) -> Transaction:
    try:
        return transaction_repository.get_transaction(transaction_id=transaction_id)
    except transaction_repository.TransactionNotFound as exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exception

@router.put(
    "/{transaction_id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def update_transaction(
    transaction_id: int,
    transaction_to_update: CreateTransaction,
    transaction_repository: Annotated[TransactionRepository, Depends(get_transaction_repository)],
) -> Transaction:
    ''' Updates an existing transaction with new data. '''
    try:
        return transaction_repository.update_transaction(
            transaction_id=transaction_id,
            transaction_to_update=transaction_to_update
        )
    except transaction_repository.TransactionNotFound as exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exception
    
@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def delete_transaction(
    transaction_id: int,
    transaction_repository: Annotated[TransactionRepository, Depends(get_transaction_repository)],
) -> dict | None:
    ''' Deletes a transaction by its ID. '''
    try:
        return transaction_repository.delete_transaction(transaction_id=transaction_id)
    except transaction_repository.TransactionNotFound as exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exception
    
@router.post("/search", status_code=status.HTTP_200_OK, responses={status.HTTP_404_NOT_FOUND: {}})
def search_transactions(
    params: TransactionSearchParams,
    transaction_repository: Annotated[TransactionRepository, Depends(get_transaction_repository)],
) -> dict | list[Transaction]:
    ''' Searches for transactions based on given parameters. '''
    return transaction_repository.search_transactions(params=params)

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_transactions(
    transaction_repository: Annotated[TransactionRepository, Depends(get_transaction_repository)],
) -> list[Transaction]:
    ''' Retrieves all transactions. '''
    return transaction_repository.get_all_transactions()