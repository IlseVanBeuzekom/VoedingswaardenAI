from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from services.shopping_list_service import ShoppingListService
from repositories.weekmenu_repository import WeekMenuRepository
from repositories.product_repository import ProductRepository
from config.database import get_db

router = APIRouter(prefix="/api/shopping-list", tags=["shopping-list"])


def get_shopping_list_service(db: Session = Depends(get_db)) -> ShoppingListService:
    weekmenu_repo = WeekMenuRepository(db)
    product_repo = ProductRepository(db)
    return ShoppingListService(weekmenu_repo, product_repo)


@router.get("/{menu_id}", response_model=List[Dict])
async def get_shopping_list(
    menu_id: int,
    shopping_service: ShoppingListService = Depends(get_shopping_list_service),
):
    try:
        shopping_list = shopping_service.generate_shopping_list(menu_id)
        return shopping_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
