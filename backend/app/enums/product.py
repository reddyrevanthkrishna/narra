from enum import Enum


class ProductStatus(str, Enum):
    """
    Represents the lifecycle state of a product.
    """

    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"