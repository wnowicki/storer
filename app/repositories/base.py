from datetime import datetime
from typing import Any, Generic, List, Type, TypeVar

from sqlmodel import Session, SQLModel, select

from app.models.base import TimeStampModel

T = TypeVar("T", bound=SQLModel)
CreateT = TypeVar("CreateT", bound=SQLModel)
UpdateT = TypeVar("UpdateT", bound=SQLModel)

GET_LIMIT = 100


class RepositoryError(Exception):
    pass


class NotFoundError(RepositoryError):
    pass


class BaseRepository(Generic[T, CreateT, UpdateT]):
    def __init__(self, model_class: Type[T], session: Session):
        self.model = model_class
        self.session = session
        self.uid_field = "id"

    def create(self, obj_in: CreateT) -> T:
        if isinstance(obj_in, dict):
            raise ValueError("obj_in must be a model instance, not a dict")

        db_obj = self.model(**obj_in.model_dump())

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def _get_core_by(self, field_name: str, field_value: Any) -> T:
        statement = (
            select(self.model).where(getattr(self.model, field_name) == field_value).limit(1)
        )
        entity = self.session.exec(statement).first()
        if entity is None:
            raise NotFoundError(f"{self.model.__name__} not found")
        return entity

    def _get_by(self, field_name: str, field_value: Any) -> T:
        return self._make(self._get_core_by(field_name, field_value))

    def get(self, entity_id: int) -> T:
        return self._get_by(self.uid_field, entity_id)

    def get_all(self, skip: int = 0, limit: int = GET_LIMIT) -> List[T]:
        statement = select(self.model).offset(skip).limit(limit)
        return list(map(self._make, self.session.exec(statement).all()))

    def _fetch_by(self, filters: dict[str, Any], skip: int = 0, limit: int = GET_LIMIT) -> List[T]:
        statement = select(self.model)
        for name, value in filters.items():
            if value is not None:
                statement = statement.where(getattr(self.model, name) == value)
        statement = statement.offset(skip).limit(limit)
        return list(map(self._make, self.session.exec(statement).all()))

    def update(self, entity_id: int, obj_in: UpdateT) -> T:
        db_obj = self._get_core_by(self.uid_field, entity_id)
        if not db_obj:
            return None

        obj_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)

        for field, value in obj_data.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)

        if isinstance(db_obj, TimeStampModel):
            db_obj.updated_at = datetime.now()

        db_obj = self.model.model_validate(db_obj)
        self.session.commit()
        return db_obj

    def delete(self, entity_id: int) -> bool:
        db_obj = self.get(entity_id)
        if not db_obj:
            return False

        self.session.delete(db_obj)
        self.session.commit()
        return True

    def _make(self, data: Any) -> T:
        """Create a new instance of the model with default values."""
        return self.model.model_validate(data)
