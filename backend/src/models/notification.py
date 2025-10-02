"""
Notification Model
Model for user notifications and alerts
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, ForeignKey,
                        String, Text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.database import BaseShared


class Notification(BaseShared):
    """
    Notification model for user alerts and reminders.

    Attributes:
        id: Notification identifier
        user_id: User who receives the notification
        type: Notification type (low_stock, expiring, meal_reminder, recipe_update, system)
        title: Notification title
        message: Notification message body
        link: Optional URL link for the notification
        is_read: Whether the notification has been read
        created_at: Notification creation timestamp
    """

    __tablename__ = "notifications"
    __table_args__ = (
        CheckConstraint(
            "type IN ('low_stock', 'expiring', 'meal_reminder', 'recipe_update', 'system')",
            name="chk_notification_type",
        ),
        {"schema": "shared"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("shared.users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    link = Column(String(255), nullable=True)
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.type}, user_id={self.user_id}, is_read={self.is_read})>"
