"""
Rating Model
Model for user recipe ratings and feedback
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Text,
                        UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.database import BaseMealPlanning


class Rating(BaseMealPlanning):
    """
    Rating model for user-specific recipe ratings.

    Each user can rate a recipe once (thumbs up/down, not averaged).

    Attributes:
        id: Rating identifier
        recipe_id: Rated recipe
        user_id: User who rated
        rating: True for thumbs up, False for thumbs down
        feedback: Optional comments
        modifications: Suggested recipe changes
        created_at: Rating creation timestamp
        updated_at: Rating update timestamp
    """

    __tablename__ = "ratings"
    __table_args__ = (
        UniqueConstraint("recipe_id", "user_id", name="uq_recipe_user_rating"),
        {"schema": "meal_planning"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipe_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meal_planning.recipes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("shared.users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rating = Column(Boolean, nullable=False, index=True)
    feedback = Column(Text, nullable=True)
    modifications = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    recipe = relationship("Recipe", back_populates="ratings")

    def __repr__(self):
        return f"<Rating(id={self.id}, recipe_id={self.recipe_id}, rating={'👍' if self.rating else '👎'})>"
