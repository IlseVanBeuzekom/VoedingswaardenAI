# backend/services/daily_food_service.py
from repositories.daily_food_repository import DailyFoodRepository
from models.daily_food_log import DailyFoodLogResponse, DailyFoodEntryCreate, DailyFoodEntryResponse
from typing import Optional
from datetime import date

class DailyFoodService:
    def __init__(self, daily_food_repo: DailyFoodRepository):
        self.daily_food_repo = daily_food_repo
    
    def get_daily_log(self, log_date: date) -> Optional[DailyFoodLogResponse]:
        """Get daily food log for a specific date"""
        db_log = self.daily_food_repo.get_daily_log_by_date(log_date)
        if not db_log:
            # Return empty log structure for the date
            return DailyFoodLogResponse(
                id=0,
                date=log_date,
                entries=[]
            )
        
        return self._format_daily_log_response(db_log)
    
    def add_entry(self, log_date: date, entry_data: DailyFoodEntryCreate) -> DailyFoodEntryResponse:
        """Add new entry to daily log"""
        db_entry = self.daily_food_repo.add_entry(log_date, entry_data)
        return self._format_entry_response(db_entry)
    
    def update_entry(self, entry_id: int, entry_data: DailyFoodEntryCreate) -> Optional[DailyFoodEntryResponse]:
        """Update existing entry"""
        db_entry = self.daily_food_repo.update_entry(entry_id, entry_data)
        return self._format_entry_response(db_entry) if db_entry else None
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete entry"""
        return self.daily_food_repo.delete_entry(entry_id)
    
    def _format_daily_log_response(self, db_log) -> DailyFoodLogResponse:
        """Format daily log with entries"""
        formatted_entries = []
        for entry in db_log.entries:
            formatted_entries.append(self._format_entry_response(entry))
        return DailyFoodLogResponse(
            id=db_log.id,
            date=db_log.date,
            entries=formatted_entries
        )
    
    def _format_entry_response(self, db_entry) -> DailyFoodEntryResponse:
        """Format entry with product/recipe info"""
        entry_data = {
            'id': db_entry.id,
            'product_id': db_entry.product_id,
            'recipe_id': db_entry.recipe_id,
            'amount': db_entry.amount,
            'unit': db_entry.unit,
            'meal_type': db_entry.meal_type,
            'product': None,
            'recipe': None
        }
        
        if db_entry.product:
            entry_data['product'] = {
                'id': db_entry.product.id,
                'name': db_entry.product.name,
                'energy_kcal': db_entry.product.energy_kcal,
                'fats': db_entry.product.fats,
                'carbohydrates': db_entry.product.carbohydrates,
                'sugars': db_entry.product.sugars,
                'fibers': db_entry.product.fibers,
                'proteins': db_entry.product.proteins,
                'serving_size': db_entry.product.serving_size
            }
        
        if db_entry.recipe:
            # Include full recipe data with ingredients for nutrition calculation
            ingredients_data = []
            for ingredient in db_entry.recipe.ingredients:
                ingredients_data.append({
                    'id': ingredient.id,
                    'product_id': ingredient.product_id,
                    'amount': ingredient.amount,
                    'unit': ingredient.unit,
                    'product': {
                        'id': ingredient.product.id,
                        'name': ingredient.product.name,
                        'energy_kcal': ingredient.product.energy_kcal,
                        'fats': ingredient.product.fats,
                        'carbohydrates': ingredient.product.carbohydrates,
                        'sugars': ingredient.product.sugars,
                        'fibers': ingredient.product.fibers,
                        'proteins': ingredient.product.proteins,
                        'serving_size': ingredient.product.serving_size
                    }
                })
            
            entry_data['recipe'] = {
                'id': db_entry.recipe.id,
                'name': db_entry.recipe.name,
                'servings': db_entry.recipe.servings,
                'ingredients': ingredients_data
            }
        
        return DailyFoodEntryResponse(**entry_data)