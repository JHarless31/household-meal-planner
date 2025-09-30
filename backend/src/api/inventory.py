"""Inventory API Routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.user import User
from src.schemas.inventory import InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse, InventoryHistoryResponse
from src.services.inventory_service import InventoryService

router = APIRouter()

@router.get("", response_model=dict)
async def list_inventory(category: Optional[str] = None, location: Optional[str] = None, low_stock: bool = False, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = InventoryService.list_items(db, category, location, low_stock)
    return {"items": [InventoryItemResponse.model_validate(i) for i in items]}

@router.post("", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory_item(item_data: InventoryItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return InventoryService.create_item(db, item_data, current_user.id)

@router.get("/{itemId}", response_model=InventoryItemResponse)
async def get_inventory_item(itemId: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = InventoryService.get_item(db, itemId)
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{itemId}", response_model=InventoryItemResponse)
async def update_inventory_item(itemId: UUID, item_data: InventoryItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = InventoryService.update_item(db, itemId, item_data, current_user.id)
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/{itemId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory_item(itemId: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not InventoryService.delete_item(db, itemId): raise HTTPException(status_code=404, detail="Item not found")

@router.get("/low-stock", response_model=dict)
async def get_low_stock(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = InventoryService.get_low_stock_items(db)
    return {"items": [InventoryItemResponse.model_validate(i) for i in items]}

@router.get("/expiring", response_model=dict)
async def get_expiring(days: int = Query(7, ge=0), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items_with_days = InventoryService.get_expiring_items(db, days)
    return {"items": [{"item": InventoryItemResponse.model_validate(item), "days_until_expiration": d} for item, d in items_with_days]}

@router.get("/{itemId}/history", response_model=dict)
async def get_item_history(itemId: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    history = InventoryService.get_item_history(db, itemId)
    return {"item_id": itemId, "history": [InventoryHistoryResponse.model_validate(h) for h in history]}
