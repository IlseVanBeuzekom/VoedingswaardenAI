from repositories.product_repository import ProductRepository
from models.product import ProductCreate, ProductResponse
from typing import List

class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo
    
    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        db_product = self.product_repo.create_product(product_data)
        return ProductResponse.from_orm(db_product)
    
    def get_all_products(self) -> List[ProductResponse]:
        db_products = self.product_repo.get_all_products()
        return [ProductResponse.from_orm(product) for product in db_products]