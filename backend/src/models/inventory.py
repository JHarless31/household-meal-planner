"""
Inventory Models
Models for inventory items and history tracking
"""

from sqlalchemy import Column, String, Numeric, Text, DateTime, ForeignKey, Date, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from src.core.database import BaseMealPlanning


class InventoryItem(BaseMealPlanning):
    """
    Inventory item model for kitchen inventory tracking.

    Attributes:
        id: Item identifier
        item_name: Item name
        quantity: Current amount
        unit: Unit of measurement
        category: Item category
        location: Storage location (pantry, fridge, freezer, other)
        expiration_date: Expiration date
        minimum_stock: Low stock threshold
        notes: Additional notes
        created_at: Item creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "inventory"
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="chk_quantity_non_negative"),
        CheckConstraint("minimum_stock >= 0", name="chk_minimum_stock_non_negative"),
        CheckConstraint("location IN ('pantry', 'fridge', 'freezer', 'other')", name="chk_location_valid"),
        {"schema": "meal_planning"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_name = Column(String(255), nullable=False, index=True)
    quantity = Column(Numeric(10, 3), default=0, nullable=False)
    unit = Column(String(50), nullable=True)
    category = Column(String(50), nullable=True, index=True)
    location = Column(String(50), nullable=True, index=True)
    expiration_date = Column(Date, nullable=True, index=True)
    minimum_stock = Column(Numeric(10, 3), default=0, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    history = relationship("InventoryHistory", back_populates="inventory_item", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InventoryItem(id={self.id}, item_name={self.item_name}, quantity={self.quantity})>"


class InventoryHistory(BaseMealPlanning):
    """
    Inventory history model for tracking quantity changes.

    Attributes:
        id: History entry identifier
        inventory_id: Parent inventory item
        change_type: Reason for change (purchased, used, expired, adjusted, auto_deducted)
        quantity_before: Quantity before change
        quantity_after: Quantity after change
        reason: Additional context
        changed_by: User who made the change
        changed_at: Change timestamp
    """
    __tablename__ = "inventory_history"
    __table_args__ = (
        CheckConstraint("change_type IN ('purchased', 'used', 'expired', 'adjusted', 'auto_deducted')", name="chk_change_type_valid"),
        {"schema": "meal_planning"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inventory_id = Column(UUID(as_uuid=True), ForeignKey("meal_planning.inventory.id", ondelete="CASCADE"), nullable=False, index=True)
    change_type = Column(String(20), nullable=False, index=True)
    quantity_before = Column(Numeric(10, 3), nullable=False)
    quantity_after = Column(Numeric(10, 3), nullable=False)
    reason = Column(String(100), nullable=True)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("shared.users.id"), nullable=True)
    changed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    # Relationships
    inventory_item = relationship("InventoryItem", back_populates="history")

    def __repr__(self):
        return f"<InventoryHistory(id={self.id}, inventory_id={self.inventory_id}, change_type={self.change_type})>"
