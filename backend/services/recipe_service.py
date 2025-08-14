from repositories.recipe_repository import RecipeRepository
from models.recipe import RecipeCreate, RecipeResponse
from typing import List, Optional


class RecipeService:
    def __init__(self, recipe_repo: RecipeRepository):
        self.recipe_repo = recipe_repo

    def create_recipe(self, recipe_data: RecipeCreate) -> RecipeResponse:
        db_recipe = self.recipe_repo.create_recipe(recipe_data)
        return self._format_recipe_response(db_recipe)

    def get_all_recipes(self) -> List[RecipeResponse]:
        db_recipes = self.recipe_repo.get_all_recipes()
        return [self._format_recipe_response(recipe) for recipe in db_recipes]

    def get_recipe_by_id(self, recipe_id: int) -> Optional[RecipeResponse]:
        db_recipe = self.recipe_repo.get_recipe_by_id(recipe_id)
        return self._format_recipe_response(db_recipe) if db_recipe else None

    def update_recipe(
        self, recipe_id: int, recipe_data: RecipeCreate
    ) -> Optional[RecipeResponse]:
        db_recipe = self.recipe_repo.update_recipe(recipe_id, recipe_data)
        return self._format_recipe_response(db_recipe) if db_recipe else None

    def delete_recipe(self, recipe_id: int) -> bool:
        return self.recipe_repo.delete_recipe(recipe_id)

    def _format_recipe_response(self, db_recipe) -> RecipeResponse:
        # Format ingredients with product info
        formatted_ingredients = []
        for ingredient in db_recipe.ingredients:
            formatted_ingredients.append(
                {
                    "id": ingredient.id,
                    "product_id": ingredient.product_id,
                    "amount": ingredient.amount,
                    "unit": ingredient.unit,
                    "product": {
                        "id": ingredient.product.id,
                        "name": ingredient.product.name,
                    },
                }
            )

        return RecipeResponse(
            id=db_recipe.id,
            name=db_recipe.name,
            servings=db_recipe.servings,
            preparation_time=db_recipe.preparation_time,
            instructions=db_recipe.instructions,
            image_url=db_recipe.image_url,
            ingredients=formatted_ingredients,
        )

    def update_recipe_image(
        self, recipe_id: int, image_url: str
    ) -> Optional[RecipeResponse]:
        db_recipe = self.recipe_repo.get_recipe_by_id(recipe_id)
        if not db_recipe:
            return None

        db_recipe.image_url = image_url
        self.recipe_repo.db.commit()
        self.recipe_repo.db.refresh(db_recipe)

        return self._format_recipe_response(db_recipe)
