"""Shopping Lists API Routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.user import User
from src.schemas.shopping_list import ShoppingListResponse
from src.services.shopping_list_service import ShoppingListService

router = APIRouter()

@router.get("/{planId}", response_model=ShoppingListResponse)
async def generate_shopping_list(planId: UUID, grouped: bool = Query(True), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return ShoppingListService.generate_shopping_list(db, planId, grouped)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
