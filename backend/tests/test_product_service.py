import pytest
from unittest.mock import Mock, patch
from models.product import ProductCreate, ProductResponse, ProductDB
from services.product_service import ProductService


class TestProductService:
    def test_create_product(self, product_service, sample_product_data):
        """Test creating product through service"""
        product_create = ProductCreate(**sample_product_data)
        result = product_service.create_product(product_create)
        
        assert isinstance(result, ProductResponse)
        assert result.name == "Test Product"
        assert result.id is not None

    def test_get_all_products_empty(self, product_service):
        """Test getting all products when none exist"""
        products = product_service.get_all_products()
        assert products == []

    def test_get_all_products(self, product_service, sample_product_data):
        """Test getting all products"""
        product_create = ProductCreate(**sample_product_data)
        product_service.create_product(product_create)
        
        products = product_service.get_all_products()
        assert len(products) == 1
        assert isinstance(products[0], ProductResponse)

    def test_get_product_by_id_exists(self, product_service, sample_product_data):
        """Test getting product by ID when it exists"""
        product_create = ProductCreate(**sample_product_data)
        created = product_service.create_product(product_create)
        
        result = product_service.get_product_by_id(created.id)
        assert result is not None
        assert result.name == "Test Product"

    def test_get_product_by_id_not_exists(self, product_service):
        """Test getting product by ID when it doesn't exist"""
        result = product_service.get_product_by_id(999)
        assert result is None

    def test_update_product_exists(self, product_service, sample_product_data):
        """Test updating existing product"""
        product_create = ProductCreate(**sample_product_data)
        created = product_service.create_product(product_create)
        
        # Update data
        sample_product_data["name"] = "Updated via Service"
        update_data = ProductCreate(**sample_product_data)
        
        result = product_service.update_product(created.id, update_data)
        assert result is not None
        assert result.name == "Updated via Service"

    def test_update_product_not_exists(self, product_service, sample_product_data):
        """Test updating non-existing product"""
        product_create = ProductCreate(**sample_product_data)
        result = product_service.update_product(999, product_create)
        assert result is None

    def test_delete_product_exists(self, product_service, sample_product_data):
        """Test deleting existing product"""
        product_create = ProductCreate(**sample_product_data)
        created = product_service.create_product(product_create)
        
        result = product_service.delete_product(created.id)
        assert result is True

    def test_delete_product_not_exists(self, product_service):
        """Test deleting non-existing product"""
        result = product_service.delete_product(999)
        assert result is False

    @patch('services.product_service.ProductResponse.from_orm')
    def test_service_calls_from_orm(self, mock_from_orm, product_service):
        """Test that service properly calls from_orm"""
        mock_db_product = Mock()
        mock_response = Mock()
        mock_from_orm.return_value = mock_response
        
        # Mock the repository method
        product_service.product_repo.get_product_by_id = Mock(return_value=mock_db_product)
        
        result = product_service.get_product_by_id(1)
        
        mock_from_orm.assert_called_once_with(mock_db_product)
        assert result == mock_response
