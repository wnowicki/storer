from datetime import datetime
from typing import Annotated

from pydantic.functional_serializers import PlainSerializer
from sqlmodel import Field, SQLModel

SerialisableDate = Annotated[datetime, PlainSerializer(lambda v: v.isoformat(), return_type=str)]


class EntityModel(SQLModel):
    """Base model with id field."""

    id: int = Field(primary_key=True)


class CreatedAtModel(EntityModel):
    """Base model with created_at timestamp."""

    created_at: SerialisableDate = Field(default_factory=datetime.now)


class TimeStampModel(CreatedAtModel):
    """Base model with created_at and updated_at timestamps."""

    updated_at: SerialisableDate | None = Field(default=None)
