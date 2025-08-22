import pytest
from pydantic import ValidationError
from models.recipe import (
    RecipeCreate, RecipeResponse, RecipeDB, 
    RecipeIngredientCreate, RecipeIngredientResponse, RecipeIngredientDB
)

class TestRecipeIngredientModels:
    def test_recipe_ingredient_create_valid_data(self, recipe_ingredient_data):
        """Test RecipeIngredientCreate with valid data"""
        ingredient = RecipeIngredientCreate(**recipe_ingredient_data)
        assert ingredient.product_id == recipe_ingredient_data["product_id"]
        assert ingredient.amount == 200.0
        assert ingredient.unit == "gram"

    def test_recipe_ingredient_create_invalid_product_id(self, recipe_ingredient_data):
        """Test RecipeIngredientCreate with invalid product_id"""
        recipe_ingredient_data["product_id"]="invalid"
        with pytest.raises(ValidationError) as exc_info:
            RecipeIngredientCreate(**recipe_ingredient_data)
        assert "Input should be a valid integer" in str(exc_info.value)

    def test_recipe_ingredient_create_negative_amount(self, recipe_ingredient_data):
        """Test RecipeIngredientCreate with negative amount"""
        recipe_ingredient_data["amount"]= -10.0
        with pytest.raises(ValidationError) as exc_info:
            RecipeIngredientCreate(**recipe_ingredient_data)
        assert "greater than 0" in str(exc_info.value)

    def test_recipe_ingredient_create_zero_amount(self, recipe_ingredient_data):
        """Test RecipeIngredientCreate with zero amount"""
        recipe_ingredient_data["amount"] = 0.0
        with pytest.raises(ValidationError) as exc_info:
            RecipeIngredientCreate(**recipe_ingredient_data)
        assert "greater than 0" in str(exc_info.value)

    def test_recipe_ingredient_create_empty_unit(self, recipe_ingredient_data):
        """Test RecipeIngredientCreate with empty unit"""
        recipe_ingredient_data["unit"] = ""
        with pytest.raises(ValidationError) as exc_info:
            RecipeIngredientCreate(**recipe_ingredient_data)
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_recipe_ingredient_create_long_unit(self, recipe_ingredient_data):
        """Test RecipeIngredientCreate with too long unit"""
        recipe_ingredient_data['unit'] = "x" * 51
        with pytest.raises(ValidationError) as exc_info:
            RecipeIngredientCreate(**recipe_ingredient_data)
        assert "String should have at most 50 characters" in str(exc_info.value)

class TestRecipeModels:
    def test_recipe_create_valid_data(self, sample_recipe_data):
        """Test RecipeCreate with valid data"""
        recipe = RecipeCreate(**sample_recipe_data)
        assert recipe.name == "Pannenkoeken"
        assert recipe.servings == 4
        assert recipe.preparation_time == 30
        assert len(recipe.ingredients) == 3

    def test_recipe_create_minimal_data(self, minimal_recipe_data):
        """Test RecipeCreate with minimal required data"""
        recipe = RecipeCreate(**minimal_recipe_data)
        assert recipe.name == "Simple Recipe"
        assert recipe.servings == 2
        assert recipe.image_url is None #Default value
        assert len(recipe.ingredients) == 1

    def test_recipe_create_empty_ingredients(self, sample_recipe_data):
        """Test RecipeCreate with empty ingredients list"""
        sample_recipe_data["ingredients"] = []
        recipe = RecipeCreate(**sample_recipe_data)
        assert len(recipe.ingredients) == 0

    def test_recipe_create_invalid_name(self, sample_recipe_data):
        """Test RecipeCreate with invalid name"""
        sample_recipe_data["name"] = ""
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(**sample_recipe_data)
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_recipe_create_long_name(self, sample_recipe_data):
        """Test RecipeCreate with too long name"""
        sample_recipe_data['name'] = 'x' * 201
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(**sample_recipe_data)
        assert "String should have at most 200 characters" in str(exc_info.value)

    def test_recipe_create_invalid_servings(self, sample_recipe_data):
        """Test RecipeCreate with invalid servings"""
        sample_recipe_data['servings'] = 0
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(**sample_recipe_data)
        assert "greater than 0" in str(exc_info.value)

    def test_recipe_create_negative_servings(self, sample_recipe_data):
        """Test RecipeCreate with negative servings"""
        sample_recipe_data['servings'] = -1
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(**sample_recipe_data)
        assert "greater than 0" in str(exc_info.value)

    def test_recipe_create_invalid_preparation_time(self, sample_recipe_data):
        """Test RecipeCreate with invalid preparation time"""
        sample_recipe_data['preparation_time'] = 0
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(**sample_recipe_data)
        assert "greater than 0" in str(exc_info.value)

    def test_recipe_create_negative_preparation_time(self, sample_recipe_data):
        """Test RecipeCreate with negative preparation time"""
        sample_recipe_data['preparation_time'] = -5
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(**sample_recipe_data)
        assert "greater than 0" in str(exc_info.value)

    def test_recipe_create_empty_instructions(self, sample_recipe_data):
        """Test RecipeCreate with empty instructions"""
        sample_recipe_data['instructions'] = ''
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(**sample_recipe_data)
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_recipe_create_with_nested_ingredient_validation(self, sample_recipe_data):
        """Test RecipeCreate with invalid nested ingredient"""
        sample_recipe_data['ingredients'][0]['amount'] = -10.0
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(**sample_recipe_data)
        assert 'greater than 0' in str(exc_info.value)

    def test_recipe_response_structure(self, sample_recipe_data):
        """Test RecipeResponse structure"""
        # Mock ingredient response data
        ingredients_response = []
        for ing in sample_recipe_data['ingredients']:
            ingredients_response.append({
                'id': 1,
                'product_id': ing['product_id'],
                'amount': ing['amount'],
                'unit': ing['unit'],
                'product': {'id': ing['product_id'], 'name': 'Test Product'}
            })
        
        recipe_response_data = {
            'id': 1,
            **sample_recipe_data,
            'ingredients': ingredients_response
        }

        response = RecipeResponse(**recipe_response_data)
        assert response.id == 1
        assert response.name == 'Pannenkoeken'
        assert len(response.ingredients) == 3

    def test_recipe_db_relationships(self, test_db, sample_products):
        """Test RecipeDB relationships"""
        # Create recipe
        recipe = RecipeDB(
            name="Test Recipe",
            servings=2,
            preparation_time=20,
            instructions="Test instructions"
        )
        test_db.add(recipe)
        test_db.flush()

        # Create ingredient
        ingredient = RecipeIngredientDB(
            recipe_id = recipe.id,
            product_id = sample_products[0].id,
            amount = 100.0,
            unit = 'gram'
        )
        test_db.add(ingredient)
        test_db.commit()

        # Test relationships
        test_db.refresh(recipe)
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0].product.name == 'Bloem'
        assert recipe.ingredients[0].recipe.name == 'Test Recipe'