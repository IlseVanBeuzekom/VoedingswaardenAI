from repositories.weekmenu_repository import WeekMenuRepository
from models.weekmenu import WeekMenuCreate, WeekMenuResponse
from typing import List, Optional
from datetime import date

class WeekMenuService:
    def __init__(self, weekmenu_repo: WeekMenuRepository):
        self.weekmenu_repo = weekmenu_repo
    
    def create_week_menu(self, menu_data: WeekMenuCreate) -> WeekMenuResponse:
        db_menu = self.weekmenu_repo.create_week_menu(menu_data)
        return self._format_menu_response(db_menu)
    
    def get_all_week_menus(self) -> List[WeekMenuResponse]:
        db_menus = self.weekmenu_repo.get_all_week_menus()
        return [self._format_menu_response(menu) for menu in db_menus]
    
    def get_week_menu_by_id(self, menu_id: int) -> Optional[WeekMenuResponse]:
        db_menu = self.weekmenu_repo.get_week_menu_by_id(menu_id)
        return self._format_menu_response(db_menu) if db_menu else None
    
    def get_week_menu_by_date_range(self, start_date: date, end_date: date) -> Optional[WeekMenuResponse]:
        db_menu = self.weekmenu_repo.get_week_menu_by_date_range(start_date, end_date)
        return self._format_menu_response(db_menu) if db_menu else None
    
    def update_week_menu(self, menu_id: int, menu_data: WeekMenuCreate) -> Optional[WeekMenuResponse]:
        db_menu = self.weekmenu_repo.update_week_menu(menu_id, menu_data)
        return self._format_menu_response(db_menu) if db_menu else None
    
    def delete_week_menu(self, menu_id: int) -> bool:
        return self.weekmenu_repo.delete_week_menu(menu_id)
    
    def _format_menu_response(self, db_menu) -> WeekMenuResponse:
        # Format days with recipe info
        formatted_days = []
        for day in db_menu.days:
            day_data = {
                'id': day.id,
                'date': day.date,
                'recipe_id': day.recipe_id,
                'servings': day.servings,
                'add_to_shopping_list': day.add_to_shopping_list,
                'recipe': None
            }
            
            if day.recipe:
                day_data['recipe'] = {
                    'id': day.recipe.id,
                    'name': day.recipe.name,
                    'servings': day.recipe.servings,
                    'preparation_time': day.recipe.preparation_time
                }
            
            formatted_days.append(day_data)
        
        # Sort days by date
        formatted_days.sort(key=lambda x: x['date'])
        
        return WeekMenuResponse(
            id=db_menu.id,
            start_date=db_menu.start_date,
            end_date=db_menu.end_date,
            days=formatted_days
        )