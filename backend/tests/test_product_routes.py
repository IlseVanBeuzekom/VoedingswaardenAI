import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import Mock, MagicMock
from routes.product_routes import router, get_product_service
from models.product import ProductCreate, ProductResponse


@pytest.fixture
def app():
    """FastAPI app fixture"""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def mock_product_service():
    """Mock product service fixture"""
    service = Mock()
    # Zorg ervoor dat alle methods Mock objecten zijn
    service.create_product = Mock()
    service.get_all_products = Mock()
    service.get_product_by_id = Mock()
    service.update_product = Mock()
    service.delete_product = Mock()
    return service


@pytest.fixture  
def client(app, mock_product_service):
    """Test client fixture with mocked service"""
    # Override de dependency met onze mock
    def override_get_product_service():
        return mock_product_service
    
    app.dependency_overrides[get_product_service] = override_get_product_service
    client = TestClient(app)
    yield client
    # Cleanup
    app.dependency_overrides = {}


class TestProductRoutes:
    def test_create_product_success(self, client, mock_product_service, sample_product_data):
        """Test successful product creation endpoint"""
        mock_response = ProductResponse(id=1, **sample_product_data)
        mock_product_service.create_product.return_value = mock_response
        
        response = client.post("/api/products/", json=sample_product_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == sample_product_data["name"]
        mock_product_service.create_product.assert_called_once()

    def test_create_product_error(self, client, mock_product_service, sample_product_data):
        """Test product creation with error"""
        mock_product_service.create_product.side_effect = Exception("Database error")
        
        response = client.post("/api/products/", json=sample_product_data)
        
        assert response.status_code == 400
        assert "Database error" in response.json()["detail"]

    def test_get_all_products(self, client, mock_product_service):
        """Test get all products endpoint"""
        mock_products = [
            ProductResponse(id=1, name="Product 1", serving_size=100, energy_kcal=200, 
                          fats=5, carbohydrates=20, sugars=10, fibers=3, proteins=15),
            ProductResponse(id=2, name="Product 2", serving_size=150, energy_kcal=250,
                          fats=8, carbohydrates=25, sugars=12, fibers=4, proteins=18)
        ]
        mock_product_service.get_all_products.return_value = mock_products
        
        response = client.get("/api/products/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Product 1"
        mock_product_service.get_all_products.assert_called_once()

    def test_get_product_exists(self, client, mock_product_service, sample_product_data):
        """Test get product by ID when it exists"""
        mock_product = ProductResponse(id=1, **sample_product_data)
        mock_product_service.get_product_by_id.return_value = mock_product
        
        response = client.get("/api/products/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == sample_product_data["name"]
        mock_product_service.get_product_by_id.assert_called_once_with(1)

    def test_get_product_not_found(self, client, mock_product_service):
        """Test get product by ID when it doesn't exist"""
        mock_product_service.get_product_by_id.return_value = None
        
        response = client.get("/api/products/999")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    def test_update_product_success(self, client, mock_product_service, sample_product_data):
        """Test successful product update"""
        mock_updated = ProductResponse(id=1, **sample_product_data)
        mock_product_service.update_product.return_value = mock_updated
        
        response = client.put("/api/products/1", json=sample_product_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        mock_product_service.update_product.assert_called_once()

    def test_update_product_not_found(self, client, mock_product_service, sample_product_data):
        """Test update non-existing product"""
        mock_product_service.update_product.return_value = None
        
        response = client.put("/api/products/999", json=sample_product_data)
        
        # De route geeft 400 terug omdat HTTPException wordt opgevangen in try-catch
        assert response.status_code == 400
        assert "404: Product not found" in response.json()["detail"]

    def test_delete_product_success(self, client, mock_product_service):
        """Test successful product deletion"""
        mock_product_service.delete_product.return_value = True
        
        response = client.delete("/api/products/1")
        
        assert response.status_code == 200
        assert response.json()["message"] == "Product successfully deleted"

    def test_delete_product_not_found(self, client, mock_product_service):
        """Test delete non-existing product"""
        mock_product_service.delete_product.return_value = False
        
        response = client.delete("/api/products/999")
        
        # De route geeft 400 terug omdat HTTPException wordt opgevangen in try-catch
        assert response.status_code == 400
        assert "404: Product not found" in response.json()["detail"]