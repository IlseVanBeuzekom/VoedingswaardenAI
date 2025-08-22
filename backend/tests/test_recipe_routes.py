import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, UploadFile
from unittest.mock import Mock, MagicMock, patch, mock_open
from io import BytesIO
from pathlib import Path

from routes.recipe_routes import router, get_recipe_service
from models.recipe import RecipeCreate, RecipeResponse

@pytest.fixture
def app():
    """FastAPI app fixture"""
    app = FastAPI()
    app.include_router(router)
    return app

@pytest.fixture
def mock_recipe_service():
    """Mock recipe service fixture"""
    service = Mock()
    service.create_recipe = Mock()
    service.get_all_recipes = Mock()
    service.get_recipe_by_id = Mock()
    service.update_recipe = Mock()
    service.delete_recipe = Mock()
    service.update_recipe_image = Mock()
    return service

@pytest.fixture
def client(app, mock_recipe_service):
    """Test client fixture with mocked service"""
    def override_get_recipe_service():
        return mock_recipe_service
    
    app.dependency_overrides[get_recipe_service] = override_get_recipe_service
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}

@pytest.fixture
def sample_recipe_response():
    """Sample recipe response for testing"""
    return RecipeResponse(
        id=1,
        name="Test Recipe",
        servings=4,
        preparation_time=30,
        instructions="Test instructions",
        image_url="/test/image.jpg",
        ingredients=[{
            "id": 1,
            "product_id": 1,
            "amount": 200.0,
            "unit": "gram",
            "product": {"id": 1, "name": "Test Product"}
        }]
    )

class TestRecipeRoutes:
    def test_create_recipe_success(self, client, mock_recipe_service, sample_recipe_data, sample_recipe_response):
        """Test successful recipe creation endpoint"""
        mock_recipe_service.create_recipe.return_value = sample_recipe_response

        response = client.post("/api/recipes/", json=sample_recipe_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Test Recipe"
        assert len(data["ingredients"]) == 1
        mock_recipe_service.create_recipe.assert_called_once()

    def test_create_recipe_error(self, client, mock_recipe_service, sample_recipe_data):
        """Test recipe creation with error"""
        mock_recipe_service.create_recipe.side_effect = Exception("Database error")

        response = client.post("/api/recipes/", json=sample_recipe_data)

        assert response.status_code == 400
        assert "Database error" in response.json()["detail"]

    def test_create_recipe_validation_error(self, client, mock_recipe_service, sample_recipe_data):
        """Test recipe creation with validation error"""
        # Remove required field
        del sample_recipe_data["name"]

        response = client.post("/api/recipes/", json=sample_recipe_data)

        assert response.status_code == 422 # Validation error
        mock_recipe_service.create_recipe.assert_not_called()

    def test_get_all_recipes_empty(self, client, mock_recipe_service):
        """Test get all recipes when none exist"""
        mock_recipe_service.get_all_recipes.return_value = []

        response = client.get('/api/recipes/')

        assert response.status_code == 200
        data = response.json()
        assert data == []
        mock_recipe_service.get_all_recipes.assert_called_once()

    def test_get_all_recipes(self, client, mock_recipe_service):
        """Test get all recipes endpoint"""
        mock_recipes = [
            RecipeResponse(
                id=1, name="Recipe 1", servings=2, preparation_time=15, instructions="Instructions 1", ingredients=[] 
            ),
            RecipeResponse(
                id=2, name="Recipe 2", servings=4, preparation_time=30,
                instructions="Instructions 2", ingredients = []
            )
        ]
        mock_recipe_service.get_all_recipes.return_value = mock_recipes

        response = client.get("/api/recipes/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Recipe 1"
        assert data[1]["name"] == "Recipe 2"

    def test_get_recipe_exists(self, client, mock_recipe_service, sample_recipe_response):
        """Test get recipe by ID when it exists"""
        mock_recipe_service.get_recipe_by_id.return_value = sample_recipe_response
        response = client.get("/api/recipes/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Test Recipe"
        mock_recipe_service.get_recipe_by_id.assert_called_once_with(1)

    def test_get_recipe_not_found(self, client, mock_recipe_service):
        """Test get recipe by ID when it doesn't exist"""
        mock_recipe_service.get_recipe_by_id.return_value = None
        response = client.get("/api/recipes/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Recipe not found"

    def test_update_recipe_success(self, client, mock_recipe_service, sample_recipe_data, sample_recipe_response):
        """Test successful recipe update"""
        mock_recipe_service.update_recipe.return_value = sample_recipe_response

        response = client.put("/api/recipes/1", json=sample_recipe_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        mock_recipe_service.update_recipe.assert_called_once()

    def test_update_recipe_not_found(self, client, mock_recipe_service, sample_recipe_data):
        """Test update non-existing recipe"""
        mock_recipe_service.update_recipe.return_value = None

        response = client.put("/api/recipes/999", json=sample_recipe_data)

        assert response.status_code == 400
        assert "Recipe not found" in response.json()["detail"]

    def test_update_recipe_error(self, client, mock_recipe_service, sample_recipe_data):
        """Test recipe update with error"""
        mock_recipe_service.update_recipe.side_effect = Exception("Update error")

        response = client.put("/api/recipes/1", json=sample_recipe_data)

        assert response.status_code == 400
        assert "Update error" in response.json()["detail"]

    def test_delete_recipe_success(self, client, mock_recipe_service):
        """Test successful recipe deletion"""
        mock_recipe_service.delete_recipe.return_value = True

        response = client.delete("/api/recipes/1")

        assert response.status_code == 200
        assert response.json()['message'] == "Recipe successfully deleted"
        mock_recipe_service.delete_recipe.assert_called_once_with(1)

    def test_delete_recipe_not_found(self, client, mock_recipe_service):
        """Test delete non-existing recipe"""
        mock_recipe_service.delete_recipe.return_value = False

        response = client.delete("/api/recipes/999")

        assert response.status_code == 400
        assert "404: Recipe not found" in response.json()["detail"]

    def test_delete_recipe_error(self, client, mock_recipe_service):
        """Test recipe deletion with error"""
        mock_recipe_service.delete_recipe.side_effect = Exception("Delete error")

        response = client.delete("/api/recipes/1")

        assert response.status_code == 400
        assert "Delete error" in response.json()['detail']

class TestRecipeImageRoutes:
    @patch("routes.recipe_routes.UPLOAD_DIR", Path("/tmp/test_uploads"))
    @patch("builtins.open", new_callable=mock_open)
    @patch("routes.recipe_routes.uuid.uuid4")
    def test_upload_recipe_image_success(self, mock_uuid, mock_file_open, client, mock_recipe_service, sample_recipe_response):
        """Test successful recipe image upload"""
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uui")

        mock_recipe_service.get_recipe_by_id.return_value = sample_recipe_response
        mock_recipe_service.update_recipe_image.return_value = sample_recipe_response

        # Create mock image file
        image_content = b"fake image data"
        files = {"file": ("test.jpg", BytesIO(image_content), "image/jpeg")}
        response = client.post('/api/recipes/1/image', files=files)

        assert response.status_code == 200
        data = response.json()
        assert "image_url" in data
        assert "/api/recipes/1/image/" in data["image_url"]
        mock_recipe_service.get_recipe_by_id.assert_called_once_with(1)
        mock_recipe_service.update_recipe_image.assert_called_once()

    def test_upload_image_recipe_not_found(self, client, mock_recipe_service):
        """Test uploading image for non-existing recipe"""
        mock_recipe_service.get_recipe_by_id.return_value = None

        files = {"file": ("test.jpg", BytesIO(b"fake data"), "image/jpeg")}
        response = client.post("/api/recipes/999/image", files=files)

        assert response.status_code == 404
        assert response.json()["detail"] == "Recipe not found"

    def test_upload_image_invalid_file_type(self, client, mock_recipe_service, sample_recipe_response):
        """Test uploading non-image file"""
        mock_recipe_service.get_recipe_by_id.return_value = sample_recipe_response

        files = {"file": ("test.txt", BytesIO(b"text data"), "text/plain")}
        response = client.post("/api/recipes/1/image", files=files)

        assert response.status_code == 400
        assert response.json()["detail"] == "File must be an image"

    @patch("routes.recipe_routes.UPLOAD_DIR", Path("/tmp/test_uploads"))
    @patch("routes.recipe_routes.FileResponse")
    def test_get_recipe_image_exists(self, mock_file_response, client):
        """Test getting recipe image when file exists"""
        mock_file_response.return_value = "file_response"

        with patch("pathlib.Path.exists", return_value=True):
            response = client.get("/api/recipes/1/image/test.jpg")

            # The actual response will be handled by FileResponse
            # We just check that the endpoint is called correctly
            mock_file_response.assert_called_once()

    def test_get_recipe_image_not_found(self, client):
        """Test getting recipe image when file doesn't exist"""
        with patch("pathlib.Path.exists", return_value=False):
            response = client.get("/api/recipes/1/image/nonexistent.jpg")

            assert response.status_code == 404
            assert response.json()["detail"] == "Image not found"

    @patch("routes.recipe_routes.UPLOAD_DIR", Path("/tmp/test_uploads"))
    @patch("builtins.open", new_callable = mock_open)
    @patch("routes.recipe_routes.uuid.uuid4")
    def test_upload_image_file_extension_handling(self, mock_uuid, mock_file_open, client, mock_recipe_service, sample_recipe_response):
        """Test that file extension is handled correctly"""
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        mock_recipe_service.get_recipe_by_id.return_value = sample_recipe_response
        mock_recipe_service.update_recipe_image.return_value = sample_recipe_response

        # Test with PNG file
        files = {"file": ("test.png", BytesIO(b"fake png data"), "image/png")}
        response = client.post("/api/recipes/1/image", files=files)

        assert response.status_code == 200
        data = response.json()
        assert data["image_url"].endswith(".png")

    @patch("routes.recipe_routes.UPLOAD_DIR", Path("/tmp/test_uploads"))
    @patch("builtins.open", new_callable=mock_open)
    @patch("routes.recipe_routes.uuid.uuid4")
    def test_upload_image_no_extension_fallback(self, mock_uuid, mock_file_open, client, mock_recipe_service, sample_recipe_response):
        """Test fallback to jpg when no file extension"""
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value = "test-uuid")

        mock_recipe_service.get_recipe_by_id.return_value = sample_recipe_response
        mock_recipe_service.update_recipe_image.return_value = sample_recipe_response

        # File without extension
        files = {"file": ("testfile", BytesIO(b"fake data"), "image/jpeg")}
        response = client.post("/api/recipes/1/image", files=files)

        assert response.status_code == 200
        data = response.json()
        assert data["image_url"].endswith(".jpg")