from __future__ import annotations

from typing import Generic, TypeVar
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.base_repository import BaseRepository


ModelType = TypeVar("ModelType")


class BaseService(Generic[ModelType]):
    def __init__(
        self,
        repository: BaseRepository[ModelType],
        entity_name: str,
    ):
        self.repository = repository
        self.entity_name = entity_name

    def get_by_id(
        self,
        db: Session,
        entity_id: UUID,
    ) -> ModelType:
        entity = self.repository.get_by_id(db, entity_id)

        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.entity_name} not found.",
            )

        return entity

    def commit(
        self,
        db: Session,
    ) -> None:
        db.commit()

    def refresh(
        self,
        db: Session,
        entity: ModelType,
    ) -> None:
        db.refresh(entity)

    def commit_and_refresh(
        self,
        db: Session,
        entity: ModelType,
) -> ModelType:
        db.commit()
        db.refresh(entity)
        return entity