"""
Recipe Models
Models for recipes, versions, ingredients, tags, and images
"""

from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey, Numeric, Date, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from src.core.database import BaseMealPlanning


class Recipe(BaseMealPlanning):
    """
    Recipe model for main recipe metadata.

    Attributes:
        id: Recipe identifier
        title: Recipe name
        description: Brief description
        source_url: Original URL if scraped
        source_type: manual or scraped
        created_by: User who created the recipe
        current_version: Latest version number
        is_deleted: Soft delete flag
        last_cooked_date: Most recent cooking date
        times_cooked: Total number of times cooked
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "recipes"
    __table_args__ = {"schema": "meal_planning"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    source_url = Column(String(500), nullable=True)
    source_type = Column(String(20), default="manual", nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("shared.users.id"), nullable=False, index=True)
    current_version = Column(Integer, default=1, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    last_cooked_date = Column(Date, nullable=True, index=True)
    times_cooked = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    versions = relationship("RecipeVersion", back_populates="recipe", cascade="all, delete-orphan", lazy="dynamic")
    tags = relationship("RecipeTag", back_populates="recipe", cascade="all, delete-orphan")
    images = relationship("RecipeImage", back_populates="recipe", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="recipe", cascade="all, delete-orphan")
    planned_meals = relationship("PlannedMeal", back_populates="recipe")

    def __repr__(self):
        return f"<Recipe(id={self.id}, title={self.title}, version={self.current_version})>"


class RecipeVersion(BaseMealPlanning):
    """
    Recipe version model for versioning system.

    Attributes:
        id: Version identifier
        recipe_id: Parent recipe
        version_number: Version sequence number
        prep_time_minutes: Preparation time
        cook_time_minutes: Cooking time
        servings: Number of servings
        difficulty: easy, medium, or hard
        instructions: Step-by-step instructions
        change_description: What changed in this version
        nutritional_info: Optional nutrition data (JSONB)
        modified_by: User who created this version
        created_at: Version creation timestamp
    """
    __tablename__ = "recipe_versions"
    __table_args__ = (
        CheckConstraint("prep_time_minutes >= 0", name="chk_prep_time_positive"),
        CheckConstraint("cook_time_minutes >= 0", name="chk_cook_time_positive"),
        CheckConstraint("servings > 0", name="chk_servings_positive"),
        CheckConstraint("difficulty IN ('easy', 'medium', 'hard')", name="chk_difficulty_valid"),
        {"schema": "meal_planning"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("meal_planning.recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    prep_time_minutes = Column(Integer, nullable=True)
    cook_time_minutes = Column(Integer, nullable=True)
    servings = Column(Integer, nullable=True)
    difficulty = Column(String(20), nullable=True)
    instructions = Column(Text, nullable=False)
    change_description = Column(Text, nullable=True)
    nutritional_info = Column(JSONB, nullable=True)
    modified_by = Column(UUID(as_uuid=True), ForeignKey("shared.users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    recipe = relationship("Recipe", back_populates="versions")
    ingredients = relationship("Ingredient", back_populates="recipe_version", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RecipeVersion(id={self.id}, recipe_id={self.recipe_id}, version={self.version_number})>"


class Ingredient(BaseMealPlanning):
    """
    Ingredient model linked to recipe versions.

    Attributes:
        id: Ingredient identifier
        recipe_version_id: Parent recipe version
        name: Ingredient name
        quantity: Amount needed
        unit: Unit of measurement
        category: Ingredient category
        display_order: Display sequence
        is_optional: Optional ingredient flag
    """
    __tablename__ = "ingredients"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="chk_quantity_positive"),
        {"schema": "meal_planning"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipe_version_id = Column(UUID(as_uuid=True), ForeignKey("meal_planning.recipe_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    quantity = Column(Numeric(10, 3), nullable=True)
    unit = Column(String(50), nullable=True)
    category = Column(String(50), nullable=True, index=True)
    display_order = Column(Integer, default=0, nullable=False)
    is_optional = Column(Boolean, default=False, nullable=False)

    # Relationships
    recipe_version = relationship("RecipeVersion", back_populates="ingredients")

    def __repr__(self):
        return f"<Ingredient(id={self.id}, name={self.name}, quantity={self.quantity})>"


class RecipeTag(BaseMealPlanning):
    """
    Recipe tag model for categorization and filtering.

    Attributes:
        id: Tag identifier
        recipe_id: Tagged recipe
        tag: Tag name
        created_at: Tag creation timestamp
    """
    __tablename__ = "recipe_tags"
    __table_args__ = {"schema": "meal_planning"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("meal_planning.recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    tag = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    recipe = relationship("Recipe", back_populates="tags")

    def __repr__(self):
        return f"<RecipeTag(id={self.id}, recipe_id={self.recipe_id}, tag={self.tag})>"


class RecipeImage(BaseMealPlanning):
    """
    Recipe image model for storing multiple images per recipe.

    Attributes:
        id: Image identifier
        recipe_id: Parent recipe
        image_path: File path or URL
        is_primary: Main recipe image flag
        display_order: Display sequence
        uploaded_by: User who uploaded image
        uploaded_at: Upload timestamp
    """
    __tablename__ = "recipe_images"
    __table_args__ = {"schema": "meal_planning"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("meal_planning.recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    image_path = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False, index=True)
    display_order = Column(Integer, default=0, nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("shared.users.id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    recipe = relationship("Recipe", back_populates="images")

    def __repr__(self):
        return f"<RecipeImage(id={self.id}, recipe_id={self.recipe_id}, is_primary={self.is_primary})>"
