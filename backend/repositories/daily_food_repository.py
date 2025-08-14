# backend/repositories/daily_food_repository.py
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date
from models.daily_food_log import (
    DailyFoodLogDB,
    DailyFoodEntryDB,
    DailyFoodLogCreate,
    DailyFoodEntryCreate,
)
from models.recipe import RecipeDB, RecipeIngredientDB


class DailyFoodRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_daily_log(self, log_date: date) -> DailyFoodLogDB:
        """Get existing daily log or create new one for the date"""
        daily_log = (
            self.db.query(DailyFoodLogDB)
            .filter(DailyFoodLogDB.date == log_date)
            .first()
        )

        if not daily_log:
            daily_log = DailyFoodLogDB(date=log_date)
            self.db.add(daily_log)
            self.db.flush()

        return daily_log

    def get_daily_log_by_date(self, log_date: date) -> Optional[DailyFoodLogDB]:
        """Get daily log with all entries for a specific date"""
        return (
            self.db.query(DailyFoodLogDB)
            .options(
                joinedload(DailyFoodLogDB.entries).joinedload(DailyFoodEntryDB.product),
                joinedload(DailyFoodLogDB.entries)
                .joinedload(DailyFoodEntryDB.recipe)
                .joinedload(RecipeDB.ingredients)
                .joinedload(RecipeIngredientDB.product),
            )
            .filter(DailyFoodLogDB.date == log_date)
            .first()
        )

    def add_entry(
        self, log_date: date, entry_data: DailyFoodEntryCreate
    ) -> DailyFoodEntryDB:
        """Add a new entry to the daily log"""
        try:
            daily_log = self.get_or_create_daily_log(log_date)

            db_entry = DailyFoodEntryDB(daily_log_id=daily_log.id, **entry_data.dict())

            self.db.add(db_entry)
            self.db.flush()  # Om direct de ID te krijgen zonder commit

            self.db.commit()
            self.db.refresh(db_entry)

            return db_entry
        except Exception as e:
            self.db.rollback()
            raise e

    def update_entry(
        self, entry_id: int, entry_data: DailyFoodEntryCreate
    ) -> Optional[DailyFoodEntryDB]:
        """Update an existing entry"""
        db_entry = (
            self.db.query(DailyFoodEntryDB)
            .filter(DailyFoodEntryDB.id == entry_id)
            .first()
        )

        if db_entry:
            db_entry.product_id = entry_data.product_id
            db_entry.recipe_id = entry_data.recipe_id
            db_entry.amount = entry_data.amount
            db_entry.unit = entry_data.unit
            db_entry.meal_type = entry_data.meal_type

            self.db.commit()
            self.db.refresh(db_entry)

        return db_entry

    def delete_entry(self, entry_id: int) -> bool:
        """Delete an entry"""
        db_entry = (
            self.db.query(DailyFoodEntryDB)
            .filter(DailyFoodEntryDB.id == entry_id)
            .first()
        )

        if db_entry:
            self.db.delete(db_entry)
            self.db.commit()
            return True
        return False
