"""Ratings API Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.user import User
from src.schemas.rating import RatingCreate, RatingResponse, RatingSummaryResponse
from src.services.rating_service import RatingService

router = APIRouter()

@router.get("/recipes/{recipeId}/ratings", response_model=dict)
async def get_recipe_ratings(recipeId: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ratings = RatingService.get_recipe_ratings(db, recipeId)
    summary = RatingService.get_rating_summary(db, recipeId)
    return {"recipe_id": recipeId, "ratings": [RatingResponse.model_validate(r) for r in ratings], "summary": summary}

@router.post("/recipes/{recipeId}/ratings", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
async def rate_recipe(recipeId: UUID, rating_data: RatingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return RatingService.create_or_update_rating(db, recipeId, current_user.id, rating_data)

@router.put("/recipes/{recipeId}/ratings/{ratingId}", response_model=RatingResponse)
async def update_rating(recipeId: UUID, ratingId: UUID, rating_data: RatingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rating = RatingService.update_rating(db, ratingId, current_user.id, rating_data)
    if not rating: raise HTTPException(status_code=404, detail="Rating not found or unauthorized")
    return rating

@router.delete("/recipes/{recipeId}/ratings/{ratingId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rating(recipeId: UUID, ratingId: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not RatingService.delete_rating(db, ratingId, current_user.id): raise HTTPException(status_code=404, detail="Rating not found or unauthorized")
