from collections.abc import Generator

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.constants import Currencies
from app.injections import get_session
from app.main import create_app
from app.models import CategoryModel, DbModel, TransactionModel


@fixture(scope="function")
def app() -> FastAPI:
    return create_app()


@fixture(scope="function")
def session(app: FastAPI) -> Generator[Session]:
    """
    Given that the FastAPI lifespan is not executed at the tests with
    the TestClient, in here a new engine is configured with another
    database file only for the tests, and then a new session is made
    per test in order to achieve isolation between tests.

    But this is not enough, we also need to tell to FastAPI that instead
    of using the already defined injection at injections.get_session, an
    override is manually made and we used the isolated session per test.
    """

    engine = create_engine("sqlite:///budget.test.db")
    DbModel.metadata.create_all(bind=engine)
    try:
        with (session := Session(bind=engine)).begin():
            app.dependency_overrides[get_session] = lambda: session
            # SQLite should raise exceptions when wrong foreign keys are used
            session.execute(text("PRAGMA foreign_keys = ON;"))
            yield session
            session.rollback()
    finally:
        DbModel.metadata.drop_all(engine)
        engine.dispose()


@fixture(scope="function")
def test_client(app: FastAPI, session: Session) -> TestClient:
    """
    The test client is a wrapper for our FastAPI instance which will
    let the tests to call the endpoints. This instance is not executing
    the already setup lifespan.
    """

    return TestClient(app=app)


# Groceries fixtures


@fixture(scope="function")
def groceries_category(session: Session) -> CategoryModel:
    category = CategoryModel(name="testing groceries category")
    session.add(category)
    session.flush()
    return category


@fixture(scope="function")
def groceries_first_euro_transaction(session: Session, groceries_category: CategoryModel) -> TransactionModel:
    transaction = TransactionModel(
        category_id=groceries_category.id,
        amount=100,
        currency=Currencies.EURO,
    )
    session.add(transaction)
    session.flush()
    return transaction


@fixture(scope="function")
def groceries_second_euro_transaction(session: Session, groceries_category: CategoryModel) -> TransactionModel:
    transaction = TransactionModel(
        category_id=groceries_category.id,
        amount=200,
        currency=Currencies.EURO,
    )
    session.add(transaction)
    session.flush()
    return transaction


# Entertainment fixtures


@fixture(scope="function")
def entertainment_category(session: Session) -> CategoryModel:
    category = CategoryModel(name="testing entertainment category")
    session.add(category)
    session.flush()
    return category


@fixture(scope="function")
def entertainment_first_lira_transaction(session: Session, entertainment_category: CategoryModel) -> TransactionModel:
    transaction = TransactionModel(
        category_id=entertainment_category.id,
        amount=2500,
        currency=Currencies.LIRA,
    )
    session.add(transaction)
    session.flush()
    return transaction


@fixture(scope="function")
def entertainment_first_rouble_transaction(session: Session, entertainment_category: CategoryModel) -> TransactionModel:
    transaction = TransactionModel(
        category_id=entertainment_category.id,
        amount=4500,
        currency=Currencies.ROUBLE,
    )
    session.add(transaction)
    session.flush()
    return transaction
