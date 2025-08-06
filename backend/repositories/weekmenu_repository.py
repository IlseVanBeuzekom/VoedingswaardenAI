from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date
from models.weekmenu import WeekMenuDB, MenuDayDB, WeekMenuCreate

class WeekMenuRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_week_menu(self, week_menu: WeekMenuCreate) -> WeekMenuDB:
        # Create week menu
        menu_data = week_menu.dict(exclude={'days'})
        db_week_menu = WeekMenuDB(**menu_data)
        self.db.add(db_week_menu)
        self.db.flush()
        
        # Add days
        for day_data in week_menu.days:
            db_day = MenuDayDB(
                week_menu_id=db_week_menu.id,
                **day_data.dict()
            )
            self.db.add(db_day)
        
        self.db.commit()
        self.db.refresh(db_week_menu)
        return db_week_menu
    
    def get_all_week_menus(self) -> List[WeekMenuDB]:
        return self.db.query(WeekMenuDB).options(
            joinedload(WeekMenuDB.days).joinedload(MenuDayDB.recipe)
        ).order_by(WeekMenuDB.start_date.desc()).all()
    
    def get_week_menu_by_id(self, menu_id: int) -> Optional[WeekMenuDB]:
        return self.db.query(WeekMenuDB).options(
            joinedload(WeekMenuDB.days).joinedload(MenuDayDB.recipe)
        ).filter(WeekMenuDB.id == menu_id).first()
    
    def get_week_menu_by_date_range(self, start_date: date, end_date: date) -> Optional[WeekMenuDB]:
        return self.db.query(WeekMenuDB).options(
            joinedload(WeekMenuDB.days).joinedload(MenuDayDB.recipe)
        ).filter(
            WeekMenuDB.start_date == start_date,
            WeekMenuDB.end_date == end_date
        ).first()

    def update_week_menu(self, menu_id: int, menu_data: WeekMenuCreate) -> Optional[WeekMenuDB]:
        db_menu = self.get_week_menu_by_id(menu_id)
        if not db_menu:
            return None
        
        # Update basic info
        menu_dict = menu_data.dict(exclude={'days'})
        for key, value in menu_dict.items():
            setattr(db_menu, key, value)
        
        # Delete existing days
        self.db.query(MenuDayDB).filter(MenuDayDB.week_menu_id == menu_id).delete()
        
        # Add new days
        for day_data in menu_data.days:
            db_day = MenuDayDB(
                week_menu_id=menu_id,
                **day_data.dict()
            )
            self.db.add(db_day)
        
        self.db.commit()
        self.db.refresh(db_menu)
        return db_menu
    
    def delete_week_menu(self, menu_id: int) -> bool:
        db_menu = self.get_week_menu_by_id(menu_id)
        if db_menu:
            self.db.delete(db_menu)
            self.db.commit()
            return True
        return False