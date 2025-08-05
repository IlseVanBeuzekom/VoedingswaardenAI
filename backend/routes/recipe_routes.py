from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.recipe import RecipeCreate, RecipeResponse
from services.recipe_service import RecipeService
from repositories.recipe_repository import RecipeRepository
from config.database import get_db

router = APIRouter(prefix="/api/recipes", tags=["recipes"])

def get_recipe_service(db: Session = Depends(get_db)) -> RecipeService:
    recipe_repo = RecipeRepository(db)
    return RecipeService(recipe_repo)

@router.post("/", response_model=RecipeResponse)
async def create_recipe(
    recipe: RecipeCreate,
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    try:
        return recipe_service.create_recipe(recipe)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[RecipeResponse])
async def get_all_recipes(
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    return recipe_service.get_all_recipes()

@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(
    recipe_id: int,
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    recipe = recipe_service.get_recipe_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: int,
    recipe: RecipeCreate,
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    try:
        updated_recipe = recipe_service.update_recipe(recipe_id, recipe)
        if not updated_recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return updated_recipe
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{recipe_id}")
async def delete_recipe(
    recipe_id: int,
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    try:
        success = recipe_service.delete_recipe(recipe_id)
        if not success:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return {"message": "Recipe successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))