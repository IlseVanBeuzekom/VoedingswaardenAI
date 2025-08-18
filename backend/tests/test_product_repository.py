import pytest
from models.product import ProductCreate, ProductDB


class TestProductRepository:
    def test_create_product(self, product_repo, sample_product_data):
        """Test creating a product"""
        product_create = ProductCreate(**sample_product_data)
        result = product_repo.create_product(product_create)
        
        assert isinstance(result, ProductDB)
        assert result.id is not None
        assert result.name == "Test Product"
        assert result.serving_size == 100.0

    def test_create_product_backward_compatibility(self, product_repo, minimal_product_data):
        """Test creating product without serving unit fields"""
        product_create = ProductCreate(**minimal_product_data)
        result = product_repo.create_product(product_create)
        
        assert result.serving_unit == "gram"
        assert result.serving_amount == 100.0  # should use serving_size

    def test_get_all_products_empty(self, product_repo):
        """Test getting all products when database is empty"""
        products = product_repo.get_all_products()
        assert products == []

    def test_get_all_products(self, product_repo, sample_product_data):
        """Test getting all products"""
        product_create = ProductCreate(**sample_product_data)
        product_repo.create_product(product_create)
        
        products = product_repo.get_all_products()
        assert len(products) == 1
        assert products[0].name == "Test Product"

    def test_get_product_by_id_exists(self, product_repo, sample_product_data):
        """Test getting product by ID when it exists"""
        product_create = ProductCreate(**sample_product_data)
        created_product = product_repo.create_product(product_create)
        
        result = product_repo.get_product_by_id(created_product.id)
        assert result is not None
        assert result.name == "Test Product"

    def test_get_product_by_id_not_exists(self, product_repo):
        """Test getting product by ID when it doesn't exist"""
        result = product_repo.get_product_by_id(999)
        assert result is None

    def test_update_product_exists(self, product_repo, sample_product_data):
        """Test updating existing product"""
        product_create = ProductCreate(**sample_product_data)
        created_product = product_repo.create_product(product_create)
        
        # Update data
        sample_product_data["name"] = "Updated Product"
        sample_product_data["energy_kcal"] = 300.0
        update_data = ProductCreate(**sample_product_data)
        
        result = product_repo.update_product(created_product.id, update_data)
        assert result is not None
        assert result.name == "Updated Product"
        assert result.energy_kcal == 300.0

    def test_update_product_not_exists(self, product_repo, sample_product_data):
        """Test updating non-existing product"""
        product_create = ProductCreate(**sample_product_data)
        result = product_repo.update_product(999, product_create)
        assert result is None

    def test_delete_product_exists(self, product_repo, sample_product_data):
        """Test deleting existing product"""
        product_create = ProductCreate(**sample_product_data)
        created_product = product_repo.create_product(product_create)
        
        result = product_repo.delete_product(created_product.id)
        assert result is True
        
        # Verify product is deleted
        deleted_product = product_repo.get_product_by_id(created_product.id)
        assert deleted_product is None

    def test_delete_product_not_exists(self, product_repo):
        """Test deleting non-existing product"""
        result = product_repo.delete_product(999)
        assert result is False

    def test_backward_compatibility_serving_fields(self, product_repo, test_db):
        """Test backward compatibility for products without serving unit fields"""
        # Create product directly in DB without serving_unit and serving_amount
        db_product = ProductDB(
            name="Legacy Product",
            serving_size=150.0,
            energy_kcal=200.0,
            fats=8.0,
            carbohydrates=25.0,
            sugars=12.0,
            fibers=4.0,
            proteins=15.0
        )
        test_db.add(db_product)
        test_db.commit()
        
        # Test get_product_by_id backward compatibility
        result = product_repo.get_product_by_id(db_product.id)
        assert result.serving_unit == "gram"
        assert result.serving_amount == 100.0
