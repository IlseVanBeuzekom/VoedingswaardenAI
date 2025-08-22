import pytest
from unittest.mock import Mock, patch
from models.recipe import RecipeCreate, RecipeResponse, RecipeDB, RecipeIngredientDB
from models.product import ProductDB
from services.recipe_service import RecipeService

class TestRecipeService:
    def test_create_recipe(self, recipe_service, sample_recipe_data):
        """Test creating recipe through service"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        result = recipe_service.create_recipe(recipe_create)

        assert isinstance(result, RecipeResponse)
        assert result.name == 'Pannenkoeken'
        assert result.id is not None
        assert len(result.ingredients) == 3

    def test_create_recipe_formats_ingredients(self, recipe_service, sample_recipe_data):
        """Test that service properly formats ingredients in response"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        result = recipe_service.create_recipe(recipe_create)
        print('result create recipe formats ingredients', result.ingredients)
        # Check ingredient formatting
        for ingredient in result.ingredients:
            print("ingredient: ", ingredient)
            if hasattr(ingredient, 'model_dump'):
                ingredient_dict = ingredient.model_dump()
            else:
                ingredient_dict = ingredient.dict()

            assert "id" in ingredient_dict
            assert "product_id" in ingredient_dict
            assert "amount" in ingredient_dict
            assert "unit" in ingredient_dict
            assert "product" in ingredient_dict
            assert "id" in ingredient_dict["product"]
            assert "name" in ingredient_dict ['product']

    def test_get_all_recipes_empty(self, recipe_service):
        """Test getting all recipes when none exist"""
        recipes = recipe_service.get_all_recipes()
        assert recipes == []

    def test_get_all_recipes(self, recipe_service, sample_recipe_data, minimal_recipe_data):
        """Test getting all recipes"""
        recipe_create1 = RecipeCreate(**sample_recipe_data)
        recipe_create2 = RecipeCreate(**minimal_recipe_data)

        recipe_service.create_recipe(recipe_create1)
        recipe_service.create_recipe(recipe_create2)

        recipes = recipe_service.get_all_recipes()
        assert len(recipes) == 2
        assert all(isinstance(recipe, RecipeResponse) for recipe in recipes)

    def test_get_recipe_by_id_exists(self, recipe_service, sample_recipe_data):
        """Test getting recipe by ID when it exists"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        created = recipe_service.create_recipe(recipe_create)

        result = recipe_service.get_recipe_by_id(created.id)
        assert result is not None
        assert result.name == 'Pannenkoeken'
        assert isinstance(result, RecipeResponse)

    def test_get_recipe_by_id_not_exists(self, recipe_service):
        """Test getting recipe by ID when it doesn't exist"""
        result = recipe_service.get_recipe_by_id(999)
        assert result is None

    def test_update_recipe_exists(self, recipe_service, sample_recipe_data):
        """Test updating existing recipe"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        created = recipe_service.create_recipe(recipe_create)

        # Update data
        sample_recipe_data['name'] = 'Updated via Service'
        sample_recipe_data['servings'] = 8
        update_data = RecipeCreate(**sample_recipe_data)

        result = recipe_service.update_recipe(created.id, update_data)
        assert result is not None
        assert result.name == 'Updated via Service'
        assert result.servings == 8

    def test_update_recipe_not_exists(self, recipe_service, sample_recipe_data):
        """Test updating non-existing recipe"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        result = recipe_service.update_recipe(999, recipe_create)
        assert result is None

    def test_delete_recipe_exists(self, recipe_service, sample_recipe_data):
        """Test deleting existing recipe"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        created = recipe_service.create_recipe(recipe_create)

        result = recipe_service.delete_recipe(created.id)
        assert result is True

    def test_delete_recipe_not_exists(self, recipe_service):
        """Test deleting non-existing recipe"""
        result = recipe_service.delete_recipe(999)
        assert result is False

    def test_update_recipe_image(self, recipe_service, sample_recipe_data):
        """Test updating recipe image"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        created = recipe_service.create_recipe(recipe_create)

        new_image_url = '/api/recipes/1/image/new_image.jpg'
        result = recipe_service.update_recipe_image(created.id, new_image_url)

        assert result is not None
        assert result.image_url == new_image_url

    def test_update_recipe_image_not_exists(self, recipe_service):
        """Test updating image for non-existing recipe"""
        result = recipe_service.update_recipe_image(999, "/some/image.jpg")
        assert result is None

    def test_format_recipe_response_with_complex_ingredients(self, recipe_service, test_db, sample_products):
        """Test _format_recipe_response with complex ingredient structure"""
        # Create a mock recipe with ingredients manually
        recipe_db = RecipeDB(
            id = 1,
            name='Test Recipe',
            servings=2,
            preparation_time=20,
            instructions='Test instructions',
            image_url="/test/image.jpg"
        )

        # Create mock ingredients with relationships
        ingredient1 = RecipeIngredientDB(
            id=1,
            recipe_id=1,
            product_id=sample_products[0].id,
            amount=100.0,
            unit='gram'
        )
        ingredient1.product = sample_products[0]
        ingredient1.recipe = recipe_db

        ingredient2 = RecipeIngredientDB(
            id=2,
            recipe_id=1,
            product_id=sample_products[1].id,
            amount=2.0,
            unit='stuk'
        )
        ingredient2.product = sample_products[1]
        ingredient2.recipe = recipe_db

        recipe_db.ingredients = [ingredient1, ingredient2]

        # Test formatting
        result = recipe_service._format_recipe_response(recipe_db)

        assert isinstance(result, RecipeResponse)
        assert result.id == 1
        assert result.name == "Test Recipe"
        assert len(result.ingredients) == 2

        # Check ingredient structure
        ing1 = result.ingredients[0].dict()
        assert ing1['id'] == 1
        assert ing1['product_id'] == sample_products[0].id
        assert ing1['amount'] == 100.0
        assert ing1['unit'] == 'gram'
        assert ing1['product']['name'] == 'Bloem'

        ing2 = result.ingredients[1].dict()
        assert ing2['id'] == 2
        assert ing2['product_id'] == sample_products[1].id
        assert ing2['amount'] == 2.0
        assert ing2['unit'] == 'stuk'
        assert ing2['product']['name'] == 'Eieren'

    @patch.object(RecipeService, '_format_recipe_response')
    def test_service_calls_format_response(self, mock_format, recipe_service):
        """Test that service methods call _format_recipe_response"""
        mock_db_recipe = Mock()
        mock_response = Mock()
        mock_format.return_value=mock_response

        # Mock the repository method
        recipe_service.recipe_repo.get_recipe_by_id = Mock(return_value=mock_db_recipe)

        result = recipe_service.get_recipe_by_id(1)

        mock_format.assert_called_once_with(mock_db_recipe)
        assert result == mock_response

    def test_service_handles_recipe_without_ingredients(self, recipe_service, sample_products):
        """Test service handles recipe with no ingredients properly"""
        recipe_data = {
            'name': 'Empty Recipe',
            'servings': 1,
            'preparation_time': 5,
            'instructions': 'Do nothing',
            'ingredients': []
        }

        recipe_create = RecipeCreate(**recipe_data)
        result = recipe_service.create_recipe(recipe_create)

        assert isinstance(result, RecipeResponse)
        assert result.name == 'Empty Recipe'
        assert result.ingredients == []

    def test_service_preserves_all_recipe_fields(self, recipe_service, sample_recipe_data):
        """Test that service preserves all recipe fields in response"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        result = recipe_service.create_recipe(recipe_create)

        # Check all fields are preserved
        assert result.name == sample_recipe_data['name']
        assert result.servings == sample_recipe_data['servings']
        assert result.preparation_time == sample_recipe_data['preparation_time']
        assert result.instructions == sample_recipe_data['instructions']
        assert result.image_url == sample_recipe_data['image_url']

    def test_create_recipe_with_ingredient_validation(self, recipe_service, sample_recipe_data):
        """Test creating recipe validates ingredients properly"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        result = recipe_service.create_recipe(recipe_create)

        # All ingredients should be properly created
        assert len(result.ingredients) == len(sample_recipe_data['ingredients'])

        for i, ingredient in enumerate(result.ingredients):
            ingredient_dict = ingredient.dict()
            expected_ingredient = sample_recipe_data['ingredients'][i]
            assert ingredient_dict['product_id'] == expected_ingredient['product_id']
            assert ingredient_dict['amount'] == expected_ingredient['amount']
            assert ingredient_dict['unit'] == expected_ingredient['unit']

    def test_update_recipe_maintains_data_integrity(self, recipe_service, sample_recipe_data, sample_products):
        """Test that updating recipe maintains data integrity"""
        # Create initial recipe
        recipe_create = RecipeCreate(**sample_recipe_data)
        created = recipe_service.create_recipe(recipe_create)

        # Update with completely different ingredients
        updated_data = {
            'name': 'Completely Different Recipe',
            'servings': 1,
            'preparation_time': 5,
            'instructions': 'New instructions',
            'ingredients': [
                {
                    'product_id': sample_products[0].id,
                    'amount': 50.0,
                    'unit': 'gram'
                }
            ]
        }

        update_recipe = RecipeCreate(**updated_data)
        result = recipe_service.update_recipe(created.id, update_recipe)

        # Verify complete update
        assert result.name == 'Completely Different Recipe'
        assert result.servings == 1
        assert len(result.ingredients) == 1
        ingredient = result.ingredients[0].dict()
        assert ingredient['amount'] == 50.0