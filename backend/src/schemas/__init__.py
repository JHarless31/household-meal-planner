"""
Pydantic Schemas
Request and response validation models
"""

from src.schemas.user import (
    UserBase, UserCreate, UserUpdate, UserResponse, UserLogin
)
from src.schemas.recipe import (
    IngredientInput, IngredientResponse,
    RecipeBase, RecipeCreate, RecipeUpdate, RecipeSummary, RecipeResponse,
    RecipeVersionResponse, ScrapedRecipeResponse
)
from src.schemas.inventory import (
    InventoryItemBase, InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse,
    InventoryHistoryResponse
)
from src.schemas.rating import (
    RatingBase, RatingCreate, RatingResponse, RatingSummaryResponse
)
from src.schemas.menu_plan import (
    PlannedMealInput, PlannedMealResponse,
    MenuPlanCreate, MenuPlanUpdate, MenuPlanResponse
)
from src.schemas.shopping_list import (
    ShoppingListItem, ShoppingListResponse
)
from src.schemas.app_settings import (
    AppSettingsResponse, AppSettingsUpdate
)
from src.schemas.common import PaginationResponse, ErrorResponse

__all__ = [
    # User
    "UserBase", "UserCreate", "UserUpdate", "UserResponse", "UserLogin",
    # Recipe
    "IngredientInput", "IngredientResponse",
    "RecipeBase", "RecipeCreate", "RecipeUpdate", "RecipeSummary", "RecipeResponse",
    "RecipeVersionResponse", "ScrapedRecipeResponse",
    # Inventory
    "InventoryItemBase", "InventoryItemCreate", "InventoryItemUpdate", "InventoryItemResponse",
    "InventoryHistoryResponse",
    # Rating
    "RatingBase", "RatingCreate", "RatingResponse", "RatingSummaryResponse",
    # Menu Plan
    "PlannedMealInput", "PlannedMealResponse",
    "MenuPlanCreate", "MenuPlanUpdate", "MenuPlanResponse",
    # Shopping List
    "ShoppingListItem", "ShoppingListResponse",
    # App Settings
    "AppSettingsResponse", "AppSettingsUpdate",
    # Common
    "PaginationResponse", "ErrorResponse",
]
