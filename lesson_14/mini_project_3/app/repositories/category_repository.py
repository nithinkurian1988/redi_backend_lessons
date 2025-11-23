from sqlalchemy import select, exists

from app.models import CategoryModel, TransactionModel
from app.repositories.base_repository import BaseSqlAlchemyRepository
from app.schemas import Category


class CategoryRepository(BaseSqlAlchemyRepository):
    def create_category(self, *, name: str) -> Category:
        # NOTE: with ORM
        new_category = CategoryModel(name=name)
        self.session.add(new_category)
        self.session.flush()
        return Category.model_validate(new_category)

    def get_categories(self) -> list[Category]:
        query = select(CategoryModel).order_by(CategoryModel.id.asc())
        results = self.session.execute(query).scalars()
        return [Category.model_validate(item) for item in results]

    def delete_category(self, *, category_id: int) -> dict | None:
        # Check if category has associated transactions
        has_transactions = self.session.execute(
            select(exists().where(TransactionModel.category_id == category_id))
        ).scalar()
        
        if has_transactions:
            return {"msg": "Cannot delete category associated with transactions. So delete the transactions first."}
        
        query = (
            select(CategoryModel)
            .filter(CategoryModel.id == category_id)
            .with_for_update()
        )
        category = self.session.execute(query).scalar_one_or_none()
        
        if category:
            self.session.delete(category)
            self.session.flush()
            return {"msg": "Category deleted successfully"}
        
        return {"msg": "Category not found"}
