from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.injections import get_category_repository
from app.repositories.category_repository import CategoryRepository
from app.schemas import Category, CreateCategory


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {}},
)
def create_category(
    category_to_create: CreateCategory,
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> Category:
    try:
        return category_repository.create_category(name=category_to_create.name)
    except Exception as exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT) from exception


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_categories(
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> list[Category]:
    return category_repository.get_categories()

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {}, status.HTTP_409_CONFLICT: {}},
)
def delete_category(
    category_id: int,
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> dict | None:
    ''' Deletes a category by its ID.'''
    return category_repository.delete_category(category_id=category_id)  