import pytest
from pydantic import ValidationError
from models.weekmenu import (
    MenuDayDB, MenuDayCreate, MenuDayResponse, 
    WeekMenuDB, WeekMenuCreate, WeekMenuResponse
)
from datetime import date, timedelta

class TestMenuDayModels:
    def test_menu_day_create_valid_data(self, menu_day_data):
        """Test MenuDayCreate with valid data"""
        menuDay = MenuDayCreate(**menu_day_data)
        assert menuDay.date == date.today()
        assert menuDay.recipe_id == 1
        assert menuDay.servings == 4
        assert menuDay.add_to_shopping_list is True

    def test_menu_day_create_missing_servings(self, menu_day_data_no_servings):
        """Test MenuDayCreate with missing servings"""
        menuDay = MenuDayCreate(**menu_day_data_no_servings)
        assert menuDay.servings is None #default

    def test_menu_day_create_invalid_date(self, menu_day_data):
        """Test MenuDayCreate with invalid date"""
        menu_day_data['date'] = 'not-a-date'
        with pytest.raises(ValidationError):
            MenuDayCreate(**menu_day_data)

    def test_menu_day_create_missing_recipe_id(self):
        """Test MenuDayCreate with missing recipe id"""
        menuDay = MenuDayCreate(
            date = date.today(),
            servings = 1,
            add_to_shopping_list=True
        )
        assert menuDay.recipe_id is None #default

class TestWeekMenuModels:
    def test_week_menu_create_valid_data(self, week_menu_data):
        """Test WeekMenuCreate with valid data"""
        weekMenu = WeekMenuCreate(**week_menu_data)
        assert weekMenu.start_date == date.today()
        assert weekMenu.end_date == date.today() + timedelta(days=1)
        assert len(weekMenu.days) == 2
        assert isinstance(weekMenu.days[0], MenuDayCreate)

    def test_week_menu_create_empty_days(self, week_menu_data):
        """Test WeekMenuCreate with empty days"""
        week_menu_data['days'] = []
        weekMenu = WeekMenuCreate(**week_menu_data)
        assert weekMenu.days == []
        assert weekMenu.start_date == date.today()
        assert weekMenu.end_date == date.today() + timedelta(days=1)

    def test_week_menu_create_with_missing_dates(self):
        """Test WeekMenuCreate with missing dates"""
        with pytest.raises(ValidationError):
            WeekMenuCreate(days=[])
    
    def test_week_menu_create_with_invalid_day(self, week_menu_data):
        """Test WeekMenuCreate with invalid days"""
        week_menu_data['days'][0]['date'] = "invalid-date"
        with pytest.raises(ValidationError):
            WeekMenuCreate(**week_menu_data)

    def test_week_menu_response_valid(self, week_menu_data):
        """Test WeekMenuResponse valid"""
        response_data = {
            "id": 1,
            "start_date": date(2025, 8, 26),
            "end_date": date(2025, 8, 30),
            "days": [
                {
                    "id": 10,
                    "date": date(2025, 8, 26),
                    "recipe_id": 2,
                    "servings": 4,
                    "add_to_shopping_list": True,
                    "recipe": {"title": "Pasta"}
                },
                {
                    "id": 11,
                    "date": date(2025, 8, 27),
                    "recipe_id": 3,
                    "servings": 2, 
                    "add_to_shopping_list": False,
                    "recipe": {"title": "Salade"}
                }
            ]
        }

        week_menu = WeekMenuResponse(**response_data)

        assert week_menu.id == 1
        assert week_menu.start_date == date(2025, 8, 26)
        assert len(week_menu.days) == 2
        assert week_menu.days[0].id == 10
        assert week_menu.days[0].recipe['title'] == 'Pasta'
        assert week_menu.days[1].add_to_shopping_list is False

    def test_week_menu_response_valid(self, week_menu_data):
        """Test WeekMenuResponse valid"""
        response_data = {
            "id": 2,
            "start_date": date(2025, 8, 26),
            "end_date": date(2025, 8, 30),
            "days": []
        }

        week_menu = WeekMenuResponse(**response_data)

        assert week_menu.id == 2
        assert week_menu.start_date == date(2025, 8, 26)
        assert week_menu.days == []

    def test_week_menu_db_relationships(self, test_db):
        """Test WeekMenuDB relationships"""
        # Create week_menu
        weekMenu = WeekMenuDB(
            start_date = date.today(),
            end_date = date.today() + timedelta(days=1)
        )

        test_db.add(weekMenu)
        test_db.flush()

        # Create MenuDay
        menuDay = MenuDayDB(
            week_menu_id = 1,
            date = date.today(),
            recipe_id = 1,
            servings = 2,
            add_to_shopping_list = True
        )
        test_db.add(menuDay)
        test_db.commit()

        # Test relationships
        test_db.refresh(weekMenu)
        assert len(weekMenu.days) == 1
        assert weekMenu.days[0].date == date.today()
        assert weekMenu.days[0].recipe_id == 1
        assert weekMenu.days[0].servings == 2
        assert weekMenu.days[0].add_to_shopping_list is True