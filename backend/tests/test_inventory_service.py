"""
Unit Tests for Inventory Service
Tests inventory CRUD operations, history tracking, and auto-deduction
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

from src.services.inventory_service import InventoryService
from src.schemas.inventory import InventoryItemCreate, InventoryItemUpdate
from src.models.inventory import InventoryItem, InventoryHistory


@pytest.mark.unit
class TestInventoryService:
    """Test cases for inventory service"""

    def test_create_item_success(self, db, test_user):
        """Test successful inventory item creation"""
        item_data = InventoryItemCreate(
            item_name="Apples",
            quantity=Decimal("10"),
            unit="pcs",
            category="fruit",
            location="fridge",
            minimum_stock=Decimal("5"),
            expiration_date=date.today() + timedelta(days=7)
        )

        item = InventoryService.create_item(db, item_data, test_user.id)

        assert item.id is not None
        assert item.item_name == "Apples"
        assert item.quantity == Decimal("10")

        # Check history was created
        history = db.query(InventoryHistory).filter(
            InventoryHistory.inventory_id == item.id
        ).first()
        assert history is not None
        assert history.change_type == "purchased"
        assert history.quantity_after == Decimal("10")

    def test_get_item_success(self, db, test_inventory_item):
        """Test successful item retrieval"""
        item = InventoryService.get_item(db, test_inventory_item.id)

        assert item is not None
        assert item.id == test_inventory_item.id

    def test_get_item_not_found(self, db):
        """Test getting non-existent item"""
        item = InventoryService.get_item(db, uuid4())

        assert item is None

    def test_list_items_all(self, db, test_inventory_items):
        """Test listing all items"""
        items = InventoryService.list_items(db)

        assert len(items) == 5

    def test_list_items_filter_category(self, db, test_inventory_items):
        """Test filtering items by category"""
        items = InventoryService.list_items(db, category="dairy")

        assert len(items) == 2
        for item in items:
            assert item.category == "dairy"

    def test_list_items_filter_location(self, db, test_inventory_items):
        """Test filtering items by location"""
        items = InventoryService.list_items(db, location="pantry")

        assert len(items) == 2
        for item in items:
            assert item.location == "pantry"

    def test_list_items_filter_low_stock(self, db, test_inventory_items):
        """Test filtering low stock items"""
        # Set one item below minimum stock
        test_inventory_items[0].quantity = Decimal("0.5")
        test_inventory_items[0].minimum_stock = Decimal("1")
        db.commit()

        items = InventoryService.list_items(db, low_stock=True)

        assert len(items) >= 1

    def test_update_item_success(self, db, test_inventory_item, test_user):
        """Test successful item update"""
        item_data = InventoryItemUpdate(
            quantity=Decimal("15"),
            location="pantry"
        )

        updated = InventoryService.update_item(
            db, test_inventory_item.id, item_data, test_user.id
        )

        assert updated is not None
        assert updated.quantity == Decimal("15")
        assert updated.location == "pantry"

        # Check history was tracked
        histories = db.query(InventoryHistory).filter(
            InventoryHistory.inventory_id == test_inventory_item.id
        ).all()
        assert len(histories) == 2  # Initial + update

    def test_update_item_quantity_tracks_history(self, db, test_inventory_item, test_user):
        """Test that quantity changes are tracked in history"""
        old_quantity = test_inventory_item.quantity

        item_data = InventoryItemUpdate(quantity=Decimal("5"))

        InventoryService.update_item(db, test_inventory_item.id, item_data, test_user.id)

        histories = db.query(InventoryHistory).filter(
            InventoryHistory.inventory_id == test_inventory_item.id,
            InventoryHistory.change_type == "adjusted"
        ).all()

        assert len(histories) == 1
        assert histories[0].quantity_before == old_quantity
        assert histories[0].quantity_after == Decimal("5")

    def test_update_item_not_found(self, db, test_user):
        """Test updating non-existent item"""
        item_data = InventoryItemUpdate(quantity=Decimal("10"))

        updated = InventoryService.update_item(db, uuid4(), item_data, test_user.id)

        assert updated is None

    def test_delete_item_success(self, db, test_inventory_item):
        """Test successful item deletion"""
        result = InventoryService.delete_item(db, test_inventory_item.id)

        assert result is True

        # Item should be deleted
        item = db.query(InventoryItem).filter(
            InventoryItem.id == test_inventory_item.id
        ).first()
        assert item is None

    def test_delete_item_not_found(self, db):
        """Test deleting non-existent item"""
        result = InventoryService.delete_item(db, uuid4())

        assert result is False

    def test_get_low_stock_items(self, db, test_inventory_items):
        """Test getting items below minimum stock"""
        # Set items to low stock
        test_inventory_items[0].quantity = Decimal("0.5")
        test_inventory_items[0].minimum_stock = Decimal("1")
        test_inventory_items[1].quantity = Decimal("3")
        test_inventory_items[1].minimum_stock = Decimal("6")
        db.commit()

        low_stock = InventoryService.get_low_stock_items(db)

        assert len(low_stock) == 2

    def test_get_expiring_items_default_days(self, db, test_inventory_items):
        """Test getting items expiring within default days"""
        # Set expiration dates
        test_inventory_items[0].expiration_date = date.today() + timedelta(days=3)
        test_inventory_items[1].expiration_date = date.today() + timedelta(days=10)
        test_inventory_items[2].expiration_date = None
        db.commit()

        expiring = InventoryService.get_expiring_items(db, days=7)

        # Should return items expiring within 7 days
        assert len(expiring) == 1
        assert expiring[0][0].id == test_inventory_items[0].id
        assert expiring[0][1] == 3  # Days until expiration

    def test_get_expiring_items_custom_days(self, db, test_inventory_items):
        """Test getting items expiring within custom days"""
        test_inventory_items[0].expiration_date = date.today() + timedelta(days=2)
        test_inventory_items[1].expiration_date = date.today() + timedelta(days=5)
        db.commit()

        expiring = InventoryService.get_expiring_items(db, days=3)

        assert len(expiring) == 1

    def test_get_item_history(self, db, test_inventory_item, test_user):
        """Test getting item history"""
        # Make some changes
        for i in range(3):
            item_data = InventoryItemUpdate(quantity=Decimal(str(10 + i)))
            InventoryService.update_item(db, test_inventory_item.id, item_data, test_user.id)

        history = InventoryService.get_item_history(db, test_inventory_item.id)

        # Should have initial + 3 updates
        assert len(history) >= 4

    def test_deduct_quantity_success(self, db, test_inventory_item, test_user):
        """Test successful quantity deduction"""
        old_quantity = test_inventory_item.quantity

        result = InventoryService.deduct_quantity(
            db,
            test_inventory_item.id,
            Decimal("3"),
            "Used for cooking",
            test_user.id
        )

        assert result is True

        # Check quantity updated
        item = db.query(InventoryItem).filter(
            InventoryItem.id == test_inventory_item.id
        ).first()
        assert item.quantity == old_quantity - Decimal("3")

        # Check history logged
        history = db.query(InventoryHistory).filter(
            InventoryHistory.inventory_id == test_inventory_item.id,
            InventoryHistory.change_type == "auto_deducted"
        ).first()
        assert history is not None
        assert history.reason == "Used for cooking"

    def test_deduct_quantity_prevents_negative(self, db, test_inventory_item, test_user):
        """Test that deduction doesn't go below zero"""
        # Try to deduct more than available
        result = InventoryService.deduct_quantity(
            db,
            test_inventory_item.id,
            Decimal("999"),
            "Test",
            test_user.id
        )

        assert result is True

        item = db.query(InventoryItem).filter(
            InventoryItem.id == test_inventory_item.id
        ).first()
        assert item.quantity == Decimal("0")

    def test_deduct_quantity_item_not_found(self, db, test_user):
        """Test deducting from non-existent item"""
        result = InventoryService.deduct_quantity(
            db, uuid4(), Decimal("5"), "Test", test_user.id
        )

        assert result is False

    def test_find_or_create_item_existing(self, db, test_inventory_item):
        """Test finding existing item"""
        item = InventoryService.find_or_create_item(
            db, test_inventory_item.item_name
        )

        assert item.id == test_inventory_item.id

    def test_find_or_create_item_case_insensitive(self, db, test_inventory_item):
        """Test finding item is case-insensitive"""
        item = InventoryService.find_or_create_item(
            db, test_inventory_item.item_name.upper()
        )

        assert item.id == test_inventory_item.id

    def test_find_or_create_item_creates_new(self, db):
        """Test creating new item when not found"""
        item = InventoryService.find_or_create_item(
            db, "New Item", unit="kg", category="other"
        )

        assert item.id is not None
        assert item.item_name == "New Item"
        assert item.quantity == Decimal("0")
        assert item.unit == "kg"
