from sqlalchemy.orm import Session
from typing import List, Optional
from models.product import ProductDB, ProductCreate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_product(self, product: ProductCreate) -> ProductDB:
        db_product = ProductDB(**product.dict())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def get_all_products(self) -> List[ProductDB]:
        return self.db.query(ProductDB).all()
    
    def get_product_by_id(self, product_id: int) -> Optional[ProductDB]:
        return self.db.query(ProductDB).filter(ProductDB.id == product_id).first()

    def update_product(self, product_id: int, product_data: ProductCreate) -> Optional[ProductDB]:
        db_product = self.get_product_by_id(product_id)
        if db_product:
            for key, value in product_data.dict().items():
                setattr(db_product, key, value)
            self.db.commit()
            self.db.refresh(db_product)
        return db_product
    
    def delete_product(self, product_id: int) -> bool:
        db_product = self.get_product_by_id(product_id)
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
            return True
        return False