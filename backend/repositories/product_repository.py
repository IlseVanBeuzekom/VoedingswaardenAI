from sqlalchemy.orm import Session
from typing import List, Optional
from models.product import ProductDB, ProductCreate


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: ProductCreate) -> ProductDB:
        product_data = product.dict()

        # Ensure backward compatibility for products without serving unit info
        if "serving_unit" not in product_data:
            product_data["serving_unit"] = "gram"
        if "serving_amount" not in product_data:
            product_data["serving_amount"] = product_data.get("serving_size", 100.0)

        db_product = ProductDB(**product_data)
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_all_products(self) -> List[ProductDB]:
        products = self.db.query(ProductDB).all()

        # Ensure backward compatibility for existing products
        for product in products:
            if not product.serving_unit:
                product.serving_unit = "gram"
            if not product.serving_amount:
                product.serving_amount = product.serving_size

        return products

    def get_product_by_id(self, product_id: int) -> Optional[ProductDB]:
        product = self.db.query(ProductDB).filter(ProductDB.id == product_id).first()

        # Ensure backward compatibility
        if product:
            if not product.serving_unit:
                product.serving_unit = "gram"
            if not product.serving_amount:
                product.serving_amount = product.serving_size

        return product

    def update_product(
        self, product_id: int, product_data: ProductCreate
    ) -> Optional[ProductDB]:
        db_product = self.get_product_by_id(product_id)
        if db_product:
            update_data = product_data.dict()

            # Ensure backward compatibility
            if "serving_unit" not in update_data:
                update_data["serving_unit"] = "gram"
            if "serving_amount" not in update_data:
                update_data["serving_amount"] = update_data.get("serving_size", 100.0)

            for key, value in update_data.items():
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
