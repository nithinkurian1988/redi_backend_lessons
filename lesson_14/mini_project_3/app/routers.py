from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.injections import get_category_repository
from app.repositories.category_repository import CategoryRepository
from app.schemas import Category, CreateCategory


category_router = APIRouter()


@category_router.post("/", status_code=status.HTTP_201_CREATED, responses={status.HTTP_409_CONFLICT: {}})
def create_category(
    category_to_create: CreateCategory,
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> Category:
    try:
        return category_repository.create_category(name=category_to_create.name)
    except Exception as exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT) from exception
