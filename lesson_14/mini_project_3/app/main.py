from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine

from app.models import DbModel
from app.routers import category_router, transaction_router, summary_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """
    This lifespan will configure the neccesary services for the app, such
    as the database base engine, and then yield until when the whole
    backend is shutdown (CTRL+C after running uvicorn) and then it will
    close the connection to the DB in order to do a clean shutdown.

    This lifespan is not executed at the tests with the TestClient, this
    one of the reasons why at the tests we configured another DB connection.
    """

    app.state.database_engine = create_engine("sqlite:///budget.db")
    DbModel.metadata.create_all(bind=app.state.database_engine)
    yield
    app.state.database_engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Budget API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(
        category_router.router,
        prefix="/categories",
        tags=["Categories"],
    )

    app.include_router(
        transaction_router.router,
        prefix="/transactions",
        tags=["Transactions"],
    )

    app.include_router(
        summary_router.router,
        prefix="/summary",
        tags=["Summary"],
    )

    return app
