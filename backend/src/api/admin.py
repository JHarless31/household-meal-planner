"""Admin API Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.core.database import get_db
from src.core.security import get_current_user, require_admin
from src.models.user import User
from src.models.app_settings import AppSettings
from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.schemas.app_settings import AppSettingsResponse, AppSettingsUpdate

router = APIRouter()

@router.get("/users", response_model=dict)
async def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    users = db.query(User).all()
    return {"users": [UserResponse.model_validate(u) for u in users]}

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    from src.core.security import SecurityManager
    user = User(username=user_data.username, email=user_data.email, password_hash=SecurityManager.hash_password(user_data.password), role=user_data.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/settings", response_model=AppSettingsResponse)
async def get_settings(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    settings = db.query(AppSettings).first()
    if not settings: raise HTTPException(status_code=404, detail="Settings not found")
    return settings

@router.put("/settings", response_model=AppSettingsResponse)
async def update_settings(settings_data: AppSettingsUpdate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    settings = db.query(AppSettings).first()
    if not settings: settings = AppSettings()
    for field, value in settings_data.model_dump().items():
        setattr(settings, field, value)
    settings.updated_by = admin.id
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings
