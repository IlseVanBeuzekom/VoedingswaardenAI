from sqlalchemy import Column, Integer, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from models.product import Base
from models.recipe import RecipeDB

class WeekMenuDB(Base):
    __tablename__ = "week_menus"
    
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    
    # Relationship to menu days
    days = relationship("MenuDayDB", back_populates="week_menu", cascade="all, delete-orphan")

class MenuDayDB(Base):
    __tablename__ = "menu_days"
    
    id = Column(Integer, primary_key=True, index=True)
    week_menu_id = Column(Integer, ForeignKey("week_menus.id"), nullable=False)
    date = Column(Date, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)
    servings = Column(Integer, nullable=False)
    add_to_shopping_list = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    week_menu = relationship("WeekMenuDB", back_populates="days")
    recipe = relationship("RecipeDB")

# Pydantic schemas
class MenuDayBase(BaseModel):
    date: date
    recipe_id: Optional[int] = None
    servings: Optional[int] = None
    add_to_shopping_list: bool = True

class MenuDayCreate(MenuDayBase):
    pass

class MenuDayResponse(MenuDayBase):
    id: int
    recipe: Optional[dict] = None  # Basic recipe info
    
    class Config:
        from_attributes = True

class WeekMenuBase(BaseModel):
    start_date: date = Field(..., description="Start date of the week")
    end_date: date = Field(..., description="End date of the week")

class WeekMenuCreate(WeekMenuBase):
    days: List[MenuDayCreate] = []

class WeekMenuResponse(WeekMenuBase):
    id: int
    days: List[MenuDayResponse] = []
    
    class Config:
        from_attributes = True