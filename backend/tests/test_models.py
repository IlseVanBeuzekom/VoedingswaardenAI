import pytest
from pydantic import ValidationError
from models.product import ProductCreate, ProductResponse, ProductDB


class TestProductModels:
    def test_product_create_valid_data(self, sample_product_data):
        """Test ProductCreate with valid data"""
        product = ProductCreate(**sample_product_data)
        assert product.name == "Test Product"
        assert product.serving_size == 100.0
        assert product.energy_kcal == 250.0

    def test_product_create_minimal_data(self, minimal_product_data):
        """Test ProductCreate with minimal required data"""
        product = ProductCreate(**minimal_product_data)
        assert product.name == "Minimal Product"
        assert product.serving_unit == "gram"  # default value
        assert product.serving_amount == 100.0  # default value

    def test_product_create_invalid_name(self, sample_product_data):
        """Test ProductCreate with invalid name"""
        sample_product_data["name"] = ""
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**sample_product_data)
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_product_create_negative_values(self, sample_product_data):
        """Test ProductCreate with negative values"""
        sample_product_data["serving_size"] = -10.0
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**sample_product_data)
        assert "greater than 0" in str(exc_info.value)

    def test_product_create_negative_nutrients(self, sample_product_data):
        """Test ProductCreate with negative nutrient values"""
        sample_product_data["fats"] = -5.0
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**sample_product_data)
        assert "greater than or equal to 0" in str(exc_info.value)

    def test_product_response_from_db(self, sample_product_data):
        """Test ProductResponse creation from DB object"""
        db_product = ProductDB(id=1, **sample_product_data)
        response = ProductResponse.from_orm(db_product)
        assert response.id == 1
        assert response.name == "Test Product"

