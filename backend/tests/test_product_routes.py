import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import Mock, patch
from routes.product_routes import router
from models.product import ProductCreate, ProductResponse


@pytest.fixture
def app():
    """FastAPI app fixture"""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    """Test client fixture"""
    return TestClient(app)


class TestProductRoutes:
    @patch('routes.product_routes.get_product_service')
    def test_create_product_success(self, mock_service_dep, client, sample_product_data):
        """Test successful product creation endpoint"""
        mock_service = Mock()
        mock_response = ProductResponse(id=1, **sample_product_data)
        mock_service.create_product.return_value = mock_response
        mock_service_dep.return_value = mock_service
        
        response = client.post("/api/products/", json=sample_product_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == sample_product_data["name"]
        mock_service.create_product.assert_called_once()

    @patch('routes.product_routes.get_product_service')
    def test_create_product_error(self, mock_service_dep, client, sample_product_data):
        """Test product creation with error"""
        mock_service = Mock()
        mock_service.create_product.side_effect = Exception("Database error")
        mock_service_dep.return_value = mock_service
        
        response = client.post("/api/products/", json=sample_product_data)
        
        assert response.status_code == 400
        assert "Database error" in response.json()["detail"]

    @patch('routes.product_routes.get_product_service')
    def test_get_all_products(self, mock_service_dep, client):
        """Test get all products endpoint"""
        mock_service = Mock()
        mock_products = [
            ProductResponse(id=1, name="Product 1", serving_size=100, energy_kcal=200, 
                          fats=5, carbohydrates=20, sugars=10, fibers=3, proteins=15),
            ProductResponse(id=2, name="Product 2", serving_size=150, energy_kcal=250,
                          fats=8, carbohydrates=25, sugars=12, fibers=4, proteins=18)
        ]
        mock_service.get_all_products.return_value = mock_products
        mock_service_dep.return_value = mock_service
        
        response = client.get("/api/products/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Product 1"
        mock_service.get_all_products.assert_called_once()

    @patch('routes.product_routes.get_product_service')
    def test_get_product_exists(self, mock_service_dep, client, sample_product_data):
        """Test get product by ID when it exists"""
        mock_service = Mock()
        mock_product = ProductResponse(id=1, **sample_product_data)
        mock_service.get_product_by_id.return_value = mock_product
        mock_service_dep.return_value = mock_service
        
        response = client.get("/api/products/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == sample_product_data["name"]
        mock_service.get_product_by_id.assert_called_once_with(1)

    @patch('routes.product_routes.get_product_service')
    def test_get_product_not_found(self, mock_service_dep, client):
        """Test get product by ID when it doesn't exist"""
        mock_service = Mock()
        mock_service.get_product_by_id.return_value = None
        mock_service_dep.return_value = mock_service
        
        response = client.get("/api/products/999")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    @patch('routes.product_routes.get_product_service')
    def test_update_product_success(self, mock_service_dep, client, sample_product_data):
        """Test successful product update"""
        mock_service = Mock()
        mock_updated = Mock()
        mock_updated.dict.return_value = {**sample_product_data, "id": 1}
        mock_service.update_product.return_value = mock_updated
        mock_service_dep.return_value = mock_service
        
        response = client.put("/api/products/1", json=sample_product_data)
        
        assert response.status_code == 200
        mock_service.update_product.assert_called_once_with(1, pytest.any(ProductCreate))

    @patch('routes.product_routes.get_product_service')
    def test_update_product_not_found(self, mock_service_dep, client, sample_product_data):
        """Test update non-existing product"""
        mock_service = Mock()
        mock_service.update_product.return_value = None
        mock_service_dep.return_value = mock_service
        
        response = client.put("/api/products/999", json=sample_product_data)
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    @patch('routes.product_routes.get_product_service')
    def test_delete_product_success(self, mock_service_dep, client):
        """Test successful product deletion"""
        mock_service = Mock()
        mock_service.delete_product.return_value = True
        mock_service_dep.return_value = mock_service
        
        response = client.delete("/api/products/1")
        
        assert response.status_code == 200
        assert response.json()["message"] == "Product successfully deleted"

    @patch('routes.product_routes.get_product_service')
    def test_delete_product_not_found(self, mock_service_dep, client):
        """Test delete non-existing product"""
        mock_service = Mock()
        mock_service.delete_product.return_value = False
        mock_service_dep.return_value = mock_service
        
        response = client.delete("/api/products/999")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"