from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from models.weekmenu import WeekMenuCreate, WeekMenuResponse
from services.weekmenu_service import WeekMenuService
from repositories.weekmenu_repository import WeekMenuRepository
from config.database import get_db

router = APIRouter(prefix="/api/weekmenus", tags=["weekmenus"])

def get_weekmenu_service(db: Session = Depends(get_db)) -> WeekMenuService:
    weekmenu_repo = WeekMenuRepository(db)
    return WeekMenuService(weekmenu_repo)

@router.post("/", response_model=WeekMenuResponse)
async def create_week_menu(
    menu: WeekMenuCreate,
    weekmenu_service: WeekMenuService = Depends(get_weekmenu_service)
):
    try:
        return weekmenu_service.create_week_menu(menu)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[WeekMenuResponse])
async def get_all_week_menus(
    weekmenu_service: WeekMenuService = Depends(get_weekmenu_service)
):
    return weekmenu_service.get_all_week_menus()

@router.get("/by-date", response_model=WeekMenuResponse)
async def get_week_menu_by_date_range(
    start_date: date = Query(...),
    end_date: date = Query(...),
    weekmenu_service: WeekMenuService = Depends(get_weekmenu_service)
):
    menu = weekmenu_service.get_week_menu_by_date_range(start_date, end_date)
    if not menu:
        return Response(status_code=status.HTTP_204_NO_CONTENT) #raise HTTPException(status_code=404, detail="Week menu not found")
    return menu

@router.get("/{menu_id}", response_model=WeekMenuResponse)
async def get_week_menu(
    menu_id: int,
    weekmenu_service: WeekMenuService = Depends(get_weekmenu_service)
):
    menu = weekmenu_service.get_week_menu_by_id(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Week menu not found")
    return menu

@router.put("/{menu_id}", response_model=WeekMenuResponse)
async def update_week_menu(
    menu_id: int,
    menu: WeekMenuCreate,
    weekmenu_service: WeekMenuService = Depends(get_weekmenu_service)
):
    try:
        updated_menu = weekmenu_service.update_week_menu(menu_id, menu)
        if not updated_menu:
            raise HTTPException(status_code=404, detail="Week menu not found")
        return updated_menu
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{menu_id}")
async def delete_week_menu(
    menu_id: int,
    weekmenu_service: WeekMenuService = Depends(get_weekmenu_service)
):
    try:
        success = weekmenu_service.delete_week_menu(menu_id)
        if not success:
            raise HTTPException(status_code=404, detail="Week menu not found")
        return {"message": "Week menu successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))