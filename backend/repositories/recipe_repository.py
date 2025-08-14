from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models.recipe import RecipeDB, RecipeIngredientDB, RecipeCreate


class RecipeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_recipe(self, recipe: RecipeCreate) -> RecipeDB:
        # Create recipe without ingredients first
        recipe_data = recipe.dict(exclude={"ingredients"})
        db_recipe = RecipeDB(**recipe_data)
        self.db.add(db_recipe)
        self.db.flush()  # Get the recipe ID

        # Add ingredients
        for ingredient_data in recipe.ingredients:
            db_ingredient = RecipeIngredientDB(
                recipe_id=db_recipe.id, **ingredient_data.dict()
            )
            self.db.add(db_ingredient)

        self.db.commit()
        self.db.refresh(db_recipe)
        return db_recipe

    def get_all_recipes(self) -> List[RecipeDB]:
        return (
            self.db.query(RecipeDB)
            .options(
                joinedload(RecipeDB.ingredients).joinedload(RecipeIngredientDB.product)
            )
            .all()
        )

    def get_recipe_by_id(self, recipe_id: int) -> Optional[RecipeDB]:
        return (
            self.db.query(RecipeDB)
            .options(
                joinedload(RecipeDB.ingredients).joinedload(RecipeIngredientDB.product)
            )
            .filter(RecipeDB.id == recipe_id)
            .first()
        )

    def update_recipe(
        self, recipe_id: int, recipe_data: RecipeCreate
    ) -> Optional[RecipeDB]:
        db_recipe = self.get_recipe_by_id(recipe_id)
        if not db_recipe:
            return None

        # Update basic recipe info
        recipe_dict = recipe_data.dict(exclude={"ingredients"})
        for key, value in recipe_dict.items():
            setattr(db_recipe, key, value)

        # Delete existing ingredients
        self.db.query(RecipeIngredientDB).filter(
            RecipeIngredientDB.recipe_id == recipe_id
        ).delete()

        # Add new ingredients
        for ingredient_data in recipe_data.ingredients:
            db_ingredient = RecipeIngredientDB(
                recipe_id=recipe_id, **ingredient_data.dict()
            )
            self.db.add(db_ingredient)

        self.db.commit()
        self.db.refresh(db_recipe)
        return db_recipe

    def delete_recipe(self, recipe_id: int) -> bool:
        db_recipe = self.get_recipe_by_id(recipe_id)
        if db_recipe:
            self.db.delete(db_recipe)
            self.db.commit()
            return True
        return False
