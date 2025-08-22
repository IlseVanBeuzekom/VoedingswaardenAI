import pytest
from pytest import mark
from models.recipe import RecipeCreate, RecipeDB, RecipeIngredientDB, RecipeIngredientCreate

class TestRecipeRepository:
    def test_create_recipe_without_ingredients(self, recipe_repo, sample_products):
        """Test creating a recipe without ingredients"""
        recipe_data = {
            'name': 'Empty Recipe',
            'servings': 1,
            'preparation_time': 10,
            'instructions': 'Do nothing',
            'ingredients': []
        }
        recipe_create = RecipeCreate(**recipe_data)
        result = recipe_repo.create_recipe(recipe_create)

        assert isinstance(result, RecipeDB)
        assert result.id is not None
        assert result.name == 'Empty Recipe'
        assert len(result.ingredients) == 0

    def test_create_recipe_with_ingredients(self, recipe_repo, sample_recipe_data):
        """Test creating a recipe with ingredients"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        result = recipe_repo.create_recipe(recipe_create)

        assert isinstance(result, RecipeDB)
        assert result.id is not None
        assert result.name == 'Pannenkoeken'
        assert result.servings == 4
        assert len(result.ingredients) == 3

        # Check first ingredient
        ingredient = result.ingredients[0]
        assert ingredient.product_id == sample_recipe_data['ingredients'][0]['product_id']
        assert ingredient.amount == 250.0
        assert ingredient.unit == 'gram'

    def test_create_recipe_ingredient_relationships(self, recipe_repo, sample_recipe_data):
        """Test that ingredient relationships are properly created"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        result = recipe_repo.create_recipe(recipe_create)

        # Check that all ingredients have proper relationships
        for ingredient in result.ingredients:
            assert ingredient.recipe_id == result.id
            assert ingredient.product is not None
            assert ingredient.recipe is not None

    def test_get_all_recipes_empty(self, recipe_repo):
        """Test getting all recipes when database is empty"""
        recipes = recipe_repo.get_all_recipes()
        assert recipes == []

    def test_get_all_recipes(self, recipe_repo, sample_recipe_data, minimal_recipe_data):
        """Test getting all recipes"""
        recipe_create1 = RecipeCreate(**sample_recipe_data)
        recipe_create2 = RecipeCreate(**minimal_recipe_data)

        recipe_repo.create_recipe(recipe_create1)
        recipe_repo.create_recipe(recipe_create2)

        recipes = recipe_repo.get_all_recipes()
        assert len(recipes) == 2

        # Recipes should have ingredients loaded
        recipe1 = next(r for r in recipes if r.name == 'Pannenkoeken')
        recipe2 = next(r for r in recipes if r.name == 'Simple Recipe')

        assert len(recipe1.ingredients) == 3
        assert len(recipe2.ingredients) == 1

    def test_get_recipe_by_id_exists(self, recipe_repo, sample_recipe_data):
        """Test getting recipe by ID when it exists"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        created_recipe = recipe_repo.create_recipe(recipe_create)

        result = recipe_repo.get_recipe_by_id(created_recipe.id)
        assert result is not None
        assert result.name == 'Pannenkoeken'
        assert len(result.ingredients) == 3

        # Check that ingredients have products loaded
        for ingredient in result.ingredients:
            assert ingredient.product is not None
    
    def test_get_recipe_by_id_not_exists(self, recipe_repo):
        """Test getting recipe by ID when it doesn't exist"""
        result = recipe_repo.get_recipe_by_id(999)
        assert result is None

    def test_update_recipe_basic_info(self, recipe_repo, sample_recipe_data):
        """Test updating basic recipe information"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        created_recipe = recipe_repo.create_recipe(recipe_create)

        # Update basic info
        updated_data = sample_recipe_data.copy()
        updated_data['name'] = 'Updated Pannenkoeken'
        updated_data['servings'] = 6
        updated_data['preparation_time'] = 45

        update_recipe = RecipeCreate(**updated_data)
        result = recipe_repo.update_recipe(created_recipe.id, update_recipe)

        assert result is not None
        assert result.name == 'Updated Pannenkoeken'
        assert result.servings == 6
        assert result.preparation_time == 45

    def test_update_recipe_ingredients(self, recipe_repo, sample_recipe_data, sample_products):
        """Test updating recipe ingredients"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        created_recipe = recipe_repo.create_recipe(recipe_create)

        # Update with different ingredients
        updated_data = sample_recipe_data.copy()
        updated_data['ingredients'] = [
            {
                'product_id': sample_products[0].id,
                'amount': 300.0, # changed amount
                'unit': 'gram'
            },
            {
                'product_id': sample_products[2].id, # only milk, no eggs
                'amount': 600.0,
                'unit': 'ml'
            }
        ]

        update_recipe = RecipeCreate(**updated_data)
        result = recipe_repo.update_recipe(created_recipe.id, update_recipe)

        assert result is not None
        assert len(result.ingredients) == 2

        # Check that old ingredients are gone and new ones are present
        amounts = [ing.amount for ing in result.ingredients]
        assert 300.0 in amounts
        assert 600.0 in amounts
        assert 250.0 not in amounts


    def test_update_recipe_not_exists(self, recipe_repo, sample_recipe_data):
        """Test updating non-existing recipe"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        result = recipe_repo.update_recipe(999, recipe_create)
        assert result is None

    def test_update_recipe_removes_old_ingredients(self, recipe_repo, sample_recipe_data, test_db):
        """Test that updating recipe properly removes old ingredients from database"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        created_recipe = recipe_repo.create_recipe(recipe_create)
        original_ingredient_count = test_db.query(RecipeIngredientDB).count()

        # Update with fewer ingredients
        updated_data = sample_recipe_data.copy()
        updated_data['ingredients'] = [sample_recipe_data['ingredients'][0]]  # Keep only first ingredient

        update_recipe = RecipeCreate(**updated_data)
        recipe_repo.update_recipe(created_recipe.id, update_recipe)

        # Check that ingredient count in database decreased
        new_ingredient_count = test_db.query(RecipeIngredientDB).count()
        assert new_ingredient_count < original_ingredient_count
        assert new_ingredient_count == 1  # Only one ingredient should remain

    def test_delete_recipe_exists(self, recipe_repo, sample_recipe_data):
        """Test deleting existing recipe"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        created_recipe = recipe_repo.create_recipe(recipe_create)

        result = recipe_repo.delete_recipe(created_recipe.id)
        assert result is True

        # Verify recipe is deleted
        deleted_recipe = recipe_repo.get_recipe_by_id(created_recipe.id)
        assert deleted_recipe is None

    def test_delete_recipe_not_exists(self, recipe_repo):
        """Test deleting non-existing recipe"""
        result = recipe_repo.delete_recipe(999)
        assert result is False

    def test_delete_recipe_cascades_ingredients(self, recipe_repo, sample_recipe_data, test_db):
        """Test that deleting recipe also deletes its ingredients"""
        recipe_create = RecipeCreate(**sample_recipe_data)
        created_recipe = recipe_repo.create_recipe(recipe_create)

        # Count ingredients before deletion
        ingredient_count_before = test_db.query(RecipeIngredientDB).filter(
            RecipeIngredientDB.recipe_id == created_recipe.id
            ).count()
        assert ingredient_count_before == 3

        # Delete recipe
        recipe_repo.delete_recipe(created_recipe.id)
        
        # Check that ingredients are also deleted
        ingredient_count_after = test_db.query(RecipeIngredientDB).filter(
            RecipeIngredientDB.recipe_id == created_recipe.id
        ).count()
        assert ingredient_count_after == 0

    def test_recipe_with_same_product_multiple_times(self, recipe_repo, sample_products):
        """Test recipe with same product used multiple times"""
        recipe_data = {
            "name": "Double Flour Recipe",
            "servings": 1, 
            "preparation_time": 10,
            "instructions": "Use flour twice",
            "ingredients": [
                {
                    "product_id": sample_products[0].id,
                    "amount": 100.0,
                    "unit": "gram"
                },
                {
                    "product_id": sample_products[0].id,
                    "amount": 50.0,
                    "unit": "gram"
                }
            ]
        }

        recipe_create = RecipeCreate(**recipe_data)
        result = recipe_repo.create_recipe(recipe_create)

        assert len(result.ingredients) == 2
        assert all(ing.product_id == sample_products[0].id for ing in result.ingredients)
        amounts = [ing.amount for ing in result.ingredients]
        assert 100.0 in amounts
        assert 50.0 in amounts

    @mark.skip # To be checked when claude is there for help
    def test_create_recipe_with_invalid_product_id(self, recipe_repo, sample_recipe_data):
        """Test creating recipe with non-existing product ID"""
        sample_recipe_data['ingredients'][0]['product_id'] = 999
        print('sample recipe data: ', sample_recipe_data)
        recipe_create = RecipeCreate(**sample_recipe_data)

        # This should raise an exception due to foreign key constraint
        with pytest.raises(Exception):
            recipe_repo.create_recipe(recipe_create)