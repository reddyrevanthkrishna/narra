from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.services.base_service import BaseService


class ProductService(BaseService[Product]):
    def __init__(self):
        super().__init__(ProductRepository())