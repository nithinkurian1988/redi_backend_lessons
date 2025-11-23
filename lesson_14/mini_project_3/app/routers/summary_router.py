from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.injections import get_summary_repository
from app.repositories.summary_repository import SummaryRepository
from app.schemas import CategorySummary


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_sumary(
    sumary_repository: Annotated[SummaryRepository, Depends(get_summary_repository)],
) -> list[CategorySummary]:
    return sumary_repository.get_sumary_per_category()
