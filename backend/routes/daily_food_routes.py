# backend/routes/daily_food_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from models.daily_food_log import (
    DailyFoodEntryCreate,
    DailyFoodLogResponse,
    DailyFoodEntryResponse,
)
from services.daily_food_service import DailyFoodService
from repositories.daily_food_repository import DailyFoodRepository
from config.database import get_db

router = APIRouter(prefix="/api/daily-food", tags=["daily-food"])


def get_daily_food_service(db: Session = Depends(get_db)) -> DailyFoodService:
    daily_food_repo = DailyFoodRepository(db)
    return DailyFoodService(daily_food_repo)


@router.get("/{log_date}", response_model=DailyFoodLogResponse)
async def get_daily_log(
    log_date: date,
    daily_food_service: DailyFoodService = Depends(get_daily_food_service),
):
    """Get daily food log for specific date"""
    return daily_food_service.get_daily_log(log_date)


@router.post("/{log_date}/entries", response_model=DailyFoodEntryResponse)
async def add_entry(
    log_date: date,
    entry: DailyFoodEntryCreate,
    daily_food_service: DailyFoodService = Depends(get_daily_food_service),
):
    """Add entry to daily log"""
    try:
        # Validate that either product_id or recipe_id is provided, not both
        if not entry.product_id and not entry.recipe_id:
            raise HTTPException(
                status_code=400,
                detail="Either product_id or recipe_id must be provided",
            )
        if entry.product_id and entry.recipe_id:
            raise HTTPException(
                status_code=400, detail="Cannot provide both product_id and recipe_id"
            )

        valid_meal_types = ["ontbijt", "lunch", "diner", "tussendoortje"]
        if entry.meal_type not in valid_meal_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid meal_type. Must be one of: {valid_meal_types}",
            )

        return daily_food_service.add_entry(log_date, entry)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/entries/{entry_id}", response_model=DailyFoodEntryResponse)
async def update_entry(
    entry_id: int,
    entry: DailyFoodEntryCreate,
    daily_food_service: DailyFoodService = Depends(get_daily_food_service),
):
    """Update existing entry"""
    try:
        # Validate that either product_id or recipe_id is provided, not both
        if not entry.product_id and not entry.recipe_id:
            raise HTTPException(
                status_code=400,
                detail="Either product_id or recipe_id must be provided",
            )
        if entry.product_id and entry.recipe_id:
            raise HTTPException(
                status_code=400, detail="Cannot provide both product_id and recipe_id"
            )

        updated_entry = daily_food_service.update_entry(entry_id, entry)
        if not updated_entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return updated_entry
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/entries/{entry_id}")
async def delete_entry(
    entry_id: int,
    daily_food_service: DailyFoodService = Depends(get_daily_food_service),
):
    """Delete entry"""
    try:
        success = daily_food_service.delete_entry(entry_id)
        if not success:
            raise HTTPException(status_code=404, detail="Entry not found")
        return {"message": "Entry successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
