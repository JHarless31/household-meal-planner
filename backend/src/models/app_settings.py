"""
App Settings Model
Model for application-specific configuration
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (CheckConstraint, Column, DateTime, ForeignKey, Integer,
                        Numeric)
from sqlalchemy.dialects.postgresql import UUID

from src.core.database import BaseMealPlanning


class AppSettings(BaseMealPlanning):
    """
    App settings model for meal planning configuration.

    Attributes:
        id: Settings identifier
        favorites_threshold: % thumbs up required for favorite (0-1, default 0.75)
        favorites_min_raters: Minimum number of raters required (default 3)
        rotation_period_days: Days before recipe considered "not recently cooked" (default 14)
        low_stock_threshold_percent: % of minimum stock for low stock alert (0-1, default 0.20)
        expiration_warning_days: Days before expiration to show warning (default 7)
        updated_by: User who last updated settings
        updated_at: Last update timestamp
    """

    __tablename__ = "app_settings"
    __table_args__ = (
        CheckConstraint(
            "favorites_threshold >= 0 AND favorites_threshold <= 1",
            name="chk_favorites_threshold_range",
        ),
        CheckConstraint(
            "favorites_min_raters > 0", name="chk_favorites_min_raters_positive"
        ),
        CheckConstraint(
            "rotation_period_days > 0", name="chk_rotation_period_positive"
        ),
        CheckConstraint(
            "low_stock_threshold_percent >= 0 AND low_stock_threshold_percent <= 1",
            name="chk_low_stock_range",
        ),
        CheckConstraint(
            "expiration_warning_days >= 0", name="chk_expiration_warning_non_negative"
        ),
        {"schema": "meal_planning"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    favorites_threshold = Column(Numeric(3, 2), default=0.75, nullable=False)
    favorites_min_raters = Column(Integer, default=3, nullable=False)
    rotation_period_days = Column(Integer, default=14, nullable=False)
    low_stock_threshold_percent = Column(Numeric(3, 2), default=0.20, nullable=False)
    expiration_warning_days = Column(Integer, default=7, nullable=False)
    updated_by = Column(
        UUID(as_uuid=True), ForeignKey("shared.users.id"), nullable=True
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return f"<AppSettings(id={self.id}, favorites_threshold={self.favorites_threshold}, rotation_period={self.rotation_period_days})>"
