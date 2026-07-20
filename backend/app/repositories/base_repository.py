from __future__ import annotations

from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def create(
        self,
        db: Session,
        entity: ModelType,
    ) -> ModelType:
        db.add(entity)
        return entity

    def get_by_id(
        self,
        db: Session,
        entity_id: UUID,
    ) -> ModelType | None:
        statement = (
            select(self.model)
            .where(self.model.id == entity_id)
        )

        return db.scalar(statement)

    def get_all(
        self,
        db: Session,
    ) -> list[ModelType]:
        statement = select(self.model)

        return list(
            db.scalars(statement).all()
        )

    def update(
        self,
        entity: ModelType,
        **kwargs,
    ) -> ModelType:
        for field, value in kwargs.items():
            setattr(entity, field, value)

        return entity

    def delete(
        self,
        db: Session,
        entity: ModelType,
    ) -> None:
        db.delete(entity)

    def soft_delete(
        self,
        entity: ModelType,
    ) -> ModelType:
        if hasattr(entity, "is_active"):
            entity.is_active = False

        return entity

    def exists(
        self,
        db: Session,
        entity_id: UUID,
    ) -> bool:
        return self.get_by_id(db, entity_id) is not None