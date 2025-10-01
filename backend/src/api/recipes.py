"""Recipe API Routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.user import User
from src.schemas.recipe import RecipeCreate, RecipeUpdate, RecipeSummary, RecipeResponse, ScrapedRecipeResponse
from src.services.recipe_service import RecipeService
from src.services.scraper import recipe_scraper
from src.services.recipe_suggestions import RecipeSuggestionService

router = APIRouter()

@router.get("", response_model=dict)
async def list_recipes(
    page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None, tags: Optional[str] = None,
    difficulty: Optional[str] = None, filter: Optional[str] = None,
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    tags_list = tags.split(',') if tags else None
    recipes, total = RecipeService.list_recipes(db, current_user.id, page, limit, search, tags_list, difficulty, filter)
    return {"recipes": [RecipeSummary.model_validate(r) for r in recipes], "pagination": {"page": page, "limit": limit, "total_pages": (total + limit - 1) // limit, "total_items": total}}

@router.post("", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe_data: RecipeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return RecipeService.create_recipe(db, recipe_data, current_user.id)

@router.get("/{recipeId}", response_model=RecipeResponse)
async def get_recipe(recipeId: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recipe = RecipeService.get_recipe(db, recipeId)
    if not recipe: raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{recipeId}", response_model=RecipeResponse)
async def update_recipe(recipeId: UUID, recipe_data: RecipeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recipe = RecipeService.update_recipe(db, recipeId, recipe_data, current_user.id)
    if not recipe: raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.delete("/{recipeId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipeId: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not RecipeService.delete_recipe(db, recipeId): raise HTTPException(status_code=404, detail="Recipe not found")

@router.post("/scrape", response_model=ScrapedRecipeResponse)
async def scrape_recipe(url_data: dict, current_user: User = Depends(get_current_user)):
    url = url_data.get("url")
    if not url: raise HTTPException(status_code=400, detail="URL required")
    recipe_data, warnings, error = recipe_scraper.scrape_recipe(url)
    if error: raise HTTPException(status_code=400, detail=error)
    if not recipe_data: raise HTTPException(status_code=400, detail="Could not scrape recipe")
    return ScrapedRecipeResponse(scraped_data=recipe_data, source_url=url, warnings=warnings)

@router.get("/suggestions", response_model=dict)
async def get_recipe_suggestions(
    strategy: str = Query("rotation", description="Suggestion strategy: rotation, favorites, never_tried, available_inventory, seasonal, quick_meals"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get intelligent recipe suggestions based on various strategies.

    Strategies:
    - rotation: Recipes not cooked recently or never tried
    - favorites: Household favorites based on ratings
    - never_tried: Recipes that have never been cooked
    - available_inventory: Recipes with most ingredients available
    - seasonal: Seasonal recipe recommendations
    - quick_meals: Fast recipes (under 30 minutes)
    """
    suggestions = RecipeSuggestionService.get_suggestions(db, current_user.id, strategy, limit)
    return {"suggestions": suggestions, "strategy": strategy, "count": len(suggestions)}
