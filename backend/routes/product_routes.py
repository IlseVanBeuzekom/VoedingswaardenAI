from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.product import ProductCreate, ProductResponse
from services.product_service import ProductService
from repositories.product_repository import ProductRepository
from config.database import get_db

router = APIRouter(prefix="/api/products", tags=["products"])

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    product_repo = ProductRepository(db)
    return ProductService(product_repo)

@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    product_service: ProductService = Depends(get_product_service)
):
    try:
        return product_service.create_product(product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ProductResponse])
async def get_all_products(
    product_service: ProductService = Depends(get_product_service)
):
    return product_service.get_all_products()
