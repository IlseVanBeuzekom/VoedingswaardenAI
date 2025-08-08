# backend/models/daily_food_log.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from models.product import Base
from models.product import ProductDB
from models.recipe import RecipeDB

class DailyFoodLogDB(Base):
    __tablename__ = "daily_food_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    
    # Relationships
    entries = relationship("DailyFoodEntryDB", back_populates="daily_log", cascade="all, delete-orphan")

class DailyFoodEntryDB(Base):
    __tablename__ = "daily_food_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    daily_log_id = Column(Integer, ForeignKey("daily_food_logs.id"), nullable=False)
    
    # Either product or recipe (not both)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)
    
    amount = Column(Float, nullable=False)
    unit = Column(String, nullable=False, default="gram")
    
    # Relationships
    daily_log = relationship("DailyFoodLogDB", back_populates="entries")
    product = relationship("ProductDB")
    recipe = relationship("RecipeDB")

# Pydantic schemas
class DailyFoodEntryBase(BaseModel):
    product_id: Optional[int] = None
    recipe_id: Optional[int] = None
    amount: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=50)

class DailyFoodEntryCreate(DailyFoodEntryBase):
    pass

class DailyFoodEntryResponse(DailyFoodEntryBase):
    id: int
    product: Optional[dict] = None
    recipe: Optional[dict] = None
    
    class Config:
        from_attributes = True

class DailyFoodLogBase(BaseModel):
    date: date

class DailyFoodLogCreate(DailyFoodLogBase):
    entries: List[DailyFoodEntryCreate] = []

class DailyFoodLogResponse(DailyFoodLogBase):
    id: int
    entries: List[DailyFoodEntryResponse] = []
    
    class Config:
        from_attributes = True