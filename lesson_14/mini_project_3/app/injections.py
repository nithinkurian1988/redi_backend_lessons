from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository
from app.repositories.summary_repository import SummaryRepository
from app.repositories.transaction_repository import TransactionRepository


def get_session(request: Request) -> Generator[Session]:
    """
    This injection will reuse the already configured database engine
    from the fastapi instance lifespan.
    """

    with (session := Session(bind=request.app.state.database_engine)).begin():
        # SQLite should raise exceptions when wrong foreign keys are used
        session.execute(text("PRAGMA foreign_keys = ON;"))
        yield session


def get_category_repository(
    session: Annotated[Session, Depends(get_session)],
) -> CategoryRepository:
    return CategoryRepository(session=session)


def get_transaction_repository(
    session: Annotated[Session, Depends(get_session)],
) -> TransactionRepository:
    return TransactionRepository(session=session)


def get_summary_repository(
    session: Annotated[Session, Depends(get_session)],
) -> SummaryRepository:
    return SummaryRepository(session=session)
