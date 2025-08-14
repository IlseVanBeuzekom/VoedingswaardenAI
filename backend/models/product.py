from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field

Base = declarative_base()


class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    serving_size = Column(
        Float, nullable=False, default=100.0
    )  # in grams (backend storage)
    serving_unit = Column(String, nullable=True, default="gram")  # display unit
    serving_amount = Column(Float, nullable=True, default=100.0)  # display amount
    energy_kcal = Column(Float, nullable=False)
    fats = Column(Float, nullable=False)
    carbohydrates = Column(Float, nullable=False)
    sugars = Column(Float, nullable=False)
    fibers = Column(Float, nullable=False)
    proteins = Column(Float, nullable=False)


# Pydantic schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    serving_size: float = Field(..., gt=0, description="Serving size in grams")
    serving_unit: str = Field(default="gram", description="Display unit for serving")
    serving_amount: float = Field(
        default=100.0, gt=0, description="Display amount for serving"
    )
    energy_kcal: float = Field(..., ge=0)
    fats: float = Field(..., ge=0)
    carbohydrates: float = Field(..., ge=0)
    sugars: float = Field(..., ge=0)
    fibers: float = Field(..., ge=0)
    proteins: float = Field(..., ge=0)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
