from repositories.product_repository import ProductRepository
from models.product import ProductCreate, ProductResponse
from typing import List, Optional

class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo
    
    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        db_product = self.product_repo.create_product(product_data)
        return ProductResponse.from_orm(db_product)
    
    def get_all_products(self) -> List[ProductResponse]:
        db_products = self.product_repo.get_all_products()
        return [ProductResponse.from_orm(product) for product in db_products]
    
    def get_product_by_id(self, product_id: int) -> Optional[ProductResponse]:
        db_product = self.product_repo.get_product_by_id(product_id)
        return ProductResponse.from_orm(db_product) if db_product else None
    
    def update_product(self, product_id: int, product_data: ProductCreate) -> Optional[ProductResponse]:
        db_product = self.product_repo.update_product(product_id, product_data)
        return ProductResponse.from_orm(db_product) if db_product else None
    
    def delete_product(self, product_id: int) -> bool:
        return self.product_repo.delete_product(product_id)
