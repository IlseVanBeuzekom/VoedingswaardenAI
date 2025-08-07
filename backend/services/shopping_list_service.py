from typing import List, Dict, Optional
from repositories.weekmenu_repository import WeekMenuRepository
from repositories.product_repository import ProductRepository

class ShoppingListService:
    def __init__(self, weekmenu_repo: WeekMenuRepository, product_repo: ProductRepository):
        self.weekmenu_repo = weekmenu_repo
        self.product_repo = product_repo
    
    def generate_shopping_list(self, menu_id: int) -> List[Dict]:
        """Generate shopping list from week menu"""
        week_menu = self.weekmenu_repo.get_week_menu_by_id(menu_id)
        if not week_menu:
            return []
        
        # Collect all ingredients with quantities
        ingredient_totals = {}
        
        for day in week_menu.days:
            if not day.recipe_id or not day.add_to_shopping_list:
                continue
                
            recipe = day.recipe
            if not recipe:
                continue
            
            # Calculate serving multiplier
            serving_multiplier = day.servings / recipe.servings if day.servings else 1
            
            # Add ingredients to totals
            for recipe_ingredient in recipe.ingredients:
                product_id = recipe_ingredient.product_id
                amount = recipe_ingredient.amount * serving_multiplier
                unit = recipe_ingredient.unit
                
                key = f"{product_id}_{unit}"
                
                if key in ingredient_totals:
                    ingredient_totals[key]['amount'] += amount
                else:
                    ingredient_totals[key] = {
                        'product_id': product_id,
                        'product_name': recipe_ingredient.product.name,
                        'amount': amount,
                        'unit': unit,
                        'checked': False
                    }
        
        # Convert to list and sort by product name
        shopping_list = list(ingredient_totals.values())
        shopping_list.sort(key=lambda x: x['product_name'])
        
        return shopping_list