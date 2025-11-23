from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.models import TransactionModel
from app.repositories.base_repository import BaseSqlAlchemyRepository
from app.schemas import CreateTransaction, Transaction, TransactionSearchParams


class TransactionRepository(BaseSqlAlchemyRepository):
    def create_transaction(self, *, transaction_to_create: CreateTransaction) -> Transaction:
        # NOTE: without ORM
        data = {
            "category_id": transaction_to_create.category_id,
            "amount": transaction_to_create.amount,
            "currency": transaction_to_create.currency,
        }
        query = insert(TransactionModel).values(**data).returning(TransactionModel)
        try:
            result = self.session.execute(query).scalar_one()
        except IntegrityError as exception:
            raise self.CategoryNotFound from exception
        return Transaction.model_validate(result)

    def get_transaction(self, *, transaction_id: int) -> Transaction:
        query = select(TransactionModel).filter(TransactionModel.id == transaction_id)
        try:
            result = self.session.execute(query).scalar_one()
        except NoResultFound as exception:
            raise self.TransactionNotFound from exception
        return Transaction.model_validate(result)
    
    def update_transaction(self, *, transaction_id: int, transaction_to_update: CreateTransaction) -> Transaction:
        query = (
            select(TransactionModel)
            .filter(TransactionModel.id == transaction_id)
            .with_for_update()
        )
        try:
            transaction_model = self.session.execute(query).scalar_one()
        except NoResultFound as exception:
            raise self.TransactionNotFound from exception
        
        transaction_model.category_id = transaction_to_update.category_id
        transaction_model.amount = transaction_to_update.amount
        transaction_model.currency = transaction_to_update.currency
        
        self.session.add(transaction_model)
        self.session.flush()
        
        return Transaction.model_validate(transaction_model)
    
    def delete_transaction(self, *, transaction_id: int) -> None:
        query = (
            select(TransactionModel)
            .filter(TransactionModel.id == transaction_id)
            .with_for_update()
        )
        try:
            transaction_model = self.session.execute(query).scalar_one()
        except NoResultFound as exception:
            raise self.TransactionNotFound from exception
        
        self.session.delete(transaction_model)
        self.session.flush()
        return {"msg": "Transaction deleted successfully."}
    
    def search_transactions(self, *, params: TransactionSearchParams) -> dict | list[Transaction]:
        query = select(TransactionModel)
        
        if params.category_id is not None:
            query = query.filter(TransactionModel.category_id == params.category_id)
        if params.min_amount is not None:
            query = query.filter(TransactionModel.amount >= params.min_amount)
        if params.max_amount is not None:
            query = query.filter(TransactionModel.amount <= params.max_amount)
        if params.currency is not None:
            query = query.filter(TransactionModel.currency == params.currency)
        
        results = self.session.execute(query).scalars().all()
        
        if not results:
            return {"msg": "Transaction not found for the provided details"}
        
        transactions = [Transaction.model_validate(item) for item in results]
        return transactions

    def get_all_transactions(self) -> list[Transaction]:
        query = select(TransactionModel).order_by(TransactionModel.id.asc())
        results = self.session.execute(query).scalars().all()
        return [Transaction.model_validate(item) for item in results]