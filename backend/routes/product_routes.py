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

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
):
    product = product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductCreate,
    product_service: ProductService = Depends(get_product_service)
):
    try:
        updated_product = product_service.update_product(product_id, product)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated_product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
):
    try:
        success = product_service.delete_product(product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))