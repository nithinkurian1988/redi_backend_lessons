from itertools import groupby
from sqlalchemy import func, select

from app.models import CategoryModel, TransactionModel
from app.repositories.base_repository import BaseSqlAlchemyRepository
from app.schemas import CategorySummary, TransactionSummary


class SummaryRepository(BaseSqlAlchemyRepository):
    def get_sumary_per_category(self) -> list[CategorySummary]:
        query = (
            select(
                CategoryModel.id.label("category_id"),
                TransactionModel.currency,
                func.sum(TransactionModel.amount).label("total"),
            )
            .join(CategoryModel, CategoryModel.id == TransactionModel.category_id)
            .group_by(CategoryModel.id, TransactionModel.currency)
            .order_by(CategoryModel.id.asc(), TransactionModel.currency.asc())
        )
        results = self.session.execute(query).mappings()
        return [
            CategorySummary(
                id=category_id,
                currencies=[
                    TransactionSummary(currency=summary.currency, total=summary.total)
                    for summary in summaries
                ],
            )
            for category_id, summaries in groupby(results, key=lambda result: result.category_id)
        ]
