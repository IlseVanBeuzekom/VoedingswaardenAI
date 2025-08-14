from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from typing import List, Optional
from models.product import Base
from models.product import ProductDB


class RecipeDB(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    servings = Column(Integer, nullable=False, default=1)
    preparation_time = Column(Integer, nullable=False)  # in minutes
    instructions = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)

    # Relationship to ingredients
    ingredients = relationship(
        "RecipeIngredientDB", back_populates="recipe", cascade="all, delete-orphan"
    )


class RecipeIngredientDB(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    amount = Column(Float, nullable=False)
    unit = Column(String, nullable=False, default="gram")  # gram, stuk, lepel, etc.

    # Relationships
    recipe = relationship("RecipeDB", back_populates="ingredients")
    product = relationship("ProductDB")


# Pydantic schemas
class RecipeIngredientBase(BaseModel):
    product_id: int
    amount: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=50)


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredientResponse(RecipeIngredientBase):
    id: int
    product: dict  # Will contain basic product info

    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    servings: int = Field(..., gt=0)
    preparation_time: int = Field(..., gt=0, description="Preparation time in minutes")
    instructions: str = Field(..., min_length=1)
    image_url: Optional[str] = None


class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientCreate] = []


class RecipeResponse(RecipeBase):
    id: int
    ingredients: List[RecipeIngredientResponse] = []

    class Config:
        from_attributes = True
