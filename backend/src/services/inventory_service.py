"""
Inventory Service
Business logic for inventory management and history tracking
"""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from uuid import UUID
from decimal import Decimal
import logging

from src.models.inventory import InventoryItem, InventoryHistory
from src.models.app_settings import AppSettings
from src.schemas.inventory import InventoryItemCreate, InventoryItemUpdate

logger = logging.getLogger(__name__)


class InventoryService:
    """Service for inventory management"""

    @staticmethod
    def create_item(db: Session, item_data: InventoryItemCreate, user_id: UUID) -> InventoryItem:
        """Create new inventory item"""
        item = InventoryItem(**item_data.model_dump())
        db.add(item)
        db.flush()

        # Log initial creation
        history = InventoryHistory(
            inventory_id=item.id,
            change_type="purchased",
            quantity_before=0,
            quantity_after=item.quantity,
            reason="Initial inventory",
            changed_by=user_id
        )
        db.add(history)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def get_item(db: Session, item_id: UUID) -> Optional[InventoryItem]:
        """Get inventory item by ID"""
        return db.query(InventoryItem).filter(InventoryItem.id == item_id).first()

    @staticmethod
    def list_items(
        db: Session,
        category: Optional[str] = None,
        location: Optional[str] = None,
        low_stock: bool = False
    ) -> List[InventoryItem]:
        """List inventory items with filters"""
        query = db.query(InventoryItem)

        if category:
            query = query.filter(InventoryItem.category == category)

        if location:
            query = query.filter(InventoryItem.location == location)

        if low_stock:
            query = query.filter(InventoryItem.quantity <= InventoryItem.minimum_stock)

        return query.all()

    @staticmethod
    def update_item(
        db: Session,
        item_id: UUID,
        item_data: InventoryItemUpdate,
        user_id: UUID
    ) -> Optional[InventoryItem]:
        """Update inventory item and track history"""
        item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item:
            return None

        old_quantity = item.quantity

        # Update fields
        for field, value in item_data.model_dump(exclude_unset=True).items():
            setattr(item, field, value)

        # Track quantity changes
        if 'quantity' in item_data.model_dump(exclude_unset=True):
            new_quantity = item_data.quantity
            if new_quantity != old_quantity:
                history = InventoryHistory(
                    inventory_id=item.id,
                    change_type="adjusted",
                    quantity_before=old_quantity,
                    quantity_after=new_quantity,
                    reason="Manual adjustment",
                    changed_by=user_id
                )
                db.add(history)

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_item(db: Session, item_id: UUID) -> bool:
        """Delete inventory item"""
        item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item:
            return False

        db.delete(item)
        db.commit()
        return True

    @staticmethod
    def get_low_stock_items(db: Session) -> List[InventoryItem]:
        """Get items below minimum stock"""
        return db.query(InventoryItem).filter(
            InventoryItem.quantity <= InventoryItem.minimum_stock
        ).all()

    @staticmethod
    def get_expiring_items(db: Session, days: int = 7) -> List[Tuple[InventoryItem, int]]:
        """Get items expiring within specified days"""
        settings = db.query(AppSettings).first()
        warning_days = settings.expiration_warning_days if settings else days

        cutoff_date = date.today() + timedelta(days=warning_days)

        items = db.query(InventoryItem).filter(
            InventoryItem.expiration_date != None,
            InventoryItem.expiration_date <= cutoff_date
        ).order_by(InventoryItem.expiration_date).all()

        # Calculate days until expiration
        result = []
        for item in items:
            days_until = (item.expiration_date - date.today()).days
            result.append((item, days_until))

        return result

    @staticmethod
    def get_item_history(db: Session, item_id: UUID) -> List[InventoryHistory]:
        """Get quantity change history for item"""
        return db.query(InventoryHistory).filter(
            InventoryHistory.inventory_id == item_id
        ).order_by(InventoryHistory.changed_at.desc()).all()

    @staticmethod
    def deduct_quantity(
        db: Session,
        item_id: UUID,
        quantity: Decimal,
        reason: str,
        user_id: Optional[UUID] = None
    ) -> bool:
        """
        Deduct quantity from inventory (for auto-deduction when meal cooked).

        Args:
            db: Database session
            item_id: Item to deduct from
            quantity: Amount to deduct
            reason: Reason for deduction
            user_id: User making the deduction

        Returns:
            bool: True if successful, False otherwise
        """
        item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item:
            return False

        old_quantity = item.quantity
        new_quantity = max(Decimal(0), old_quantity - quantity)

        item.quantity = new_quantity

        # Log history
        history = InventoryHistory(
            inventory_id=item.id,
            change_type="auto_deducted",
            quantity_before=old_quantity,
            quantity_after=new_quantity,
            reason=reason,
            changed_by=user_id
        )
        db.add(history)
        db.commit()

        return True

    @staticmethod
    def find_or_create_item(
        db: Session,
        name: str,
        unit: Optional[str] = None,
        category: Optional[str] = None
    ) -> InventoryItem:
        """Find existing item by name or create new one"""
        # Try to find existing item
        item = db.query(InventoryItem).filter(
            InventoryItem.item_name.ilike(name)
        ).first()

        if item:
            return item

        # Create new item with zero quantity
        item = InventoryItem(
            item_name=name,
            quantity=Decimal(0),
            unit=unit,
            category=category
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
