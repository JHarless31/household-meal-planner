"""
Pydantic Schemas
Request and response validation models
"""

from src.schemas.app_settings import AppSettingsResponse, AppSettingsUpdate
from src.schemas.common import ErrorResponse, PaginationResponse
from src.schemas.inventory import (InventoryHistoryResponse, InventoryItemBase,
                                   InventoryItemCreate, InventoryItemResponse,
                                   InventoryItemUpdate)
from src.schemas.menu_plan import (MenuPlanCreate, MenuPlanResponse,
                                   MenuPlanUpdate, PlannedMealInput,
                                   PlannedMealResponse)
from src.schemas.rating import (RatingBase, RatingCreate, RatingResponse,
                                RatingSummaryResponse)
from src.schemas.recipe import (IngredientInput, IngredientResponse,
                                RecipeBase, RecipeCreate, RecipeResponse,
                                RecipeSummary, RecipeUpdate,
                                RecipeVersionResponse, ScrapedRecipeResponse)
from src.schemas.shopping_list import ShoppingListItem, ShoppingListResponse
from src.schemas.user import (UserBase, UserCreate, UserLogin, UserResponse,
                              UserUpdate)

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    # Recipe
    "IngredientInput",
    "IngredientResponse",
    "RecipeBase",
    "RecipeCreate",
    "RecipeUpdate",
    "RecipeSummary",
    "RecipeResponse",
    "RecipeVersionResponse",
    "ScrapedRecipeResponse",
    # Inventory
    "InventoryItemBase",
    "InventoryItemCreate",
    "InventoryItemUpdate",
    "InventoryItemResponse",
    "InventoryHistoryResponse",
    # Rating
    "RatingBase",
    "RatingCreate",
    "RatingResponse",
    "RatingSummaryResponse",
    # Menu Plan
    "PlannedMealInput",
    "PlannedMealResponse",
    "MenuPlanCreate",
    "MenuPlanUpdate",
    "MenuPlanResponse",
    # Shopping List
    "ShoppingListItem",
    "ShoppingListResponse",
    # App Settings
    "AppSettingsResponse",
    "AppSettingsUpdate",
    # Common
    "PaginationResponse",
    "ErrorResponse",
]
