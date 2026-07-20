from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class BaseEntity(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    Base,
):
    __abstract__ = True