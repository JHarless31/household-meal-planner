"""
Menu Planning Models
Models for weekly menu plans and planned meals
"""

from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey, Date, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from src.core.database import BaseMealPlanning


class MenuPlan(BaseMealPlanning):
    """
    Menu plan model for weekly meal planning.

    Attributes:
        id: Menu plan identifier
        week_start_date: Monday of the week
        name: Optional plan name
        created_by: User who created the plan
        is_active: Active plan flag
        created_at: Plan creation timestamp
        updated_at: Plan update timestamp
    """
    __tablename__ = "menu_plans"
    __table_args__ = (
        CheckConstraint("EXTRACT(ISODOW FROM week_start_date) = 1", name="chk_week_start_monday"),
        {"schema": "meal_planning"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    week_start_date = Column(Date, nullable=False, index=True)
    name = Column(String(100), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("shared.users.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    meals = relationship("PlannedMeal", back_populates="menu_plan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MenuPlan(id={self.id}, week_start={self.week_start_date}, name={self.name})>"


class PlannedMeal(BaseMealPlanning):
    """
    Planned meal model for individual meals in menu plans.

    Attributes:
        id: Planned meal identifier
        menu_plan_id: Parent menu plan
        recipe_id: Recipe to cook
        meal_date: Date of the meal
        meal_type: Meal slot (breakfast, lunch, dinner, snack)
        servings_planned: Number of servings to make
        notes: Meal notes
        cooked: Whether meal was cooked
        cooked_date: When meal was marked cooked
        cooked_by: User who cooked the meal
    """
    __tablename__ = "planned_meals"
    __table_args__ = (
        CheckConstraint("meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')", name="chk_meal_type_valid"),
        CheckConstraint("servings_planned > 0", name="chk_servings_positive"),
        {"schema": "meal_planning"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    menu_plan_id = Column(UUID(as_uuid=True), ForeignKey("meal_planning.menu_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("meal_planning.recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    meal_date = Column(Date, nullable=False, index=True)
    meal_type = Column(String(20), nullable=False)
    servings_planned = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    cooked = Column(Boolean, default=False, nullable=False, index=True)
    cooked_date = Column(DateTime(timezone=True), nullable=True)
    cooked_by = Column(UUID(as_uuid=True), ForeignKey("shared.users.id"), nullable=True)

    # Relationships
    menu_plan = relationship("MenuPlan", back_populates="meals")
    recipe = relationship("Recipe", back_populates="planned_meals")

    def __repr__(self):
        return f"<PlannedMeal(id={self.id}, recipe_id={self.recipe_id}, date={self.meal_date}, type={self.meal_type})>"
