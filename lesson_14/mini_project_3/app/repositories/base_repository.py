from sqlalchemy.orm import Session


class BaseSqlAlchemyRepository:
    session: Session

    class TransactionNotFound(Exception): ...

    class CategoryNotFound(Exception): ...

    def __init__(self, *, session: Session):
        self.session = session
