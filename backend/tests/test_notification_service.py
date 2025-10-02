"""
Unit Tests for Notification Service
Tests notification creation, management, and automated generation
"""

from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from src.models.inventory import InventoryItem
from src.models.menu_plan import MenuPlan, PlannedMeal
from src.models.notification import Notification
from src.services.notification_service import NotificationService


@pytest.mark.unit
class TestNotificationService:
    """Test cases for notification service"""

    def test_create_notification_success(self, db, test_user):
        """Test successful notification creation"""
        notif = NotificationService.create_notification(
            db,
            test_user.id,
            "low_stock",
            "Low Stock Alert",
            "Item running low",
            "/inventory",
        )

        assert notif.id is not None
        assert notif.user_id == test_user.id
        assert notif.type == "low_stock"
        assert notif.is_read is False

    def test_get_user_notifications_all(self, db, test_user):
        """Test getting all user notifications"""
        # Create multiple notifications
        for i in range(3):
            NotificationService.create_notification(
                db, test_user.id, "test", f"Test {i}", f"Message {i}"
            )

        notifs = NotificationService.get_user_notifications(db, test_user.id)

        assert len(notifs) == 3

    def test_get_user_notifications_unread_only(self, db, test_user):
        """Test getting only unread notifications"""
        # Create notifications
        notif1 = NotificationService.create_notification(
            db, test_user.id, "test", "Test 1", "Message 1"
        )
        notif2 = NotificationService.create_notification(
            db, test_user.id, "test", "Test 2", "Message 2"
        )

        # Mark one as read
        notif1.is_read = True
        db.commit()

        notifs = NotificationService.get_user_notifications(
            db, test_user.id, unread_only=True
        )

        assert len(notifs) == 1
        assert notifs[0].id == notif2.id

    def test_get_user_notifications_limit(self, db, test_user):
        """Test notification limit"""
        # Create many notifications
        for i in range(10):
            NotificationService.create_notification(
                db, test_user.id, "test", f"Test {i}", f"Message {i}"
            )

        notifs = NotificationService.get_user_notifications(db, test_user.id, limit=5)

        assert len(notifs) == 5

    def test_mark_as_read_success(self, db, test_notification, test_user):
        """Test marking notification as read"""
        updated = NotificationService.mark_as_read(
            db, test_notification.id, test_user.id
        )

        assert updated is not None
        assert updated.is_read is True

    def test_mark_as_read_unauthorized(self, db, test_notification, admin_user):
        """Test user cannot mark another user's notification as read"""
        updated = NotificationService.mark_as_read(
            db, test_notification.id, admin_user.id
        )

        assert updated is None

    def test_mark_as_read_not_found(self, db, test_user):
        """Test marking non-existent notification as read"""
        updated = NotificationService.mark_as_read(db, uuid4(), test_user.id)

        assert updated is None

    def test_mark_all_as_read(self, db, test_user):
        """Test marking all notifications as read"""
        # Create notifications
        for i in range(5):
            NotificationService.create_notification(
                db, test_user.id, "test", f"Test {i}", f"Message {i}"
            )

        count = NotificationService.mark_all_as_read(db, test_user.id)

        assert count == 5

        # Check all marked read
        unread = (
            db.query(Notification)
            .filter(Notification.user_id == test_user.id, Notification.is_read == False)
            .count()
        )
        assert unread == 0

    def test_delete_notification_success(self, db, test_notification, test_user):
        """Test successful notification deletion"""
        result = NotificationService.delete_notification(
            db, test_notification.id, test_user.id
        )

        assert result is True

        notif = (
            db.query(Notification)
            .filter(Notification.id == test_notification.id)
            .first()
        )
        assert notif is None

    def test_delete_notification_unauthorized(self, db, test_notification, admin_user):
        """Test user cannot delete another user's notification"""
        result = NotificationService.delete_notification(
            db, test_notification.id, admin_user.id
        )

        assert result is False

    def test_get_unread_count(self, db, test_user):
        """Test getting unread notification count"""
        # Create notifications
        notif1 = NotificationService.create_notification(
            db, test_user.id, "test", "Test 1", "Message 1"
        )
        notif2 = NotificationService.create_notification(
            db, test_user.id, "test", "Test 2", "Message 2"
        )
        notif3 = NotificationService.create_notification(
            db, test_user.id, "test", "Test 3", "Message 3"
        )

        # Mark one as read
        notif1.is_read = True
        db.commit()

        count = NotificationService.get_unread_count(db, test_user.id)

        assert count == 2

    def test_generate_low_stock_notifications(self, db, test_user):
        """Test generating low stock notifications"""
        # Create low stock item
        item = InventoryItem(
            item_name="Low Stock Item",
            quantity=Decimal("1"),
            unit="pcs",
            category="other",
            threshold=Decimal("10"),
        )
        db.add(item)
        db.commit()

        count = NotificationService.generate_low_stock_notifications(db)

        assert count >= 1

        # Check notification created
        notif = (
            db.query(Notification)
            .filter(
                Notification.user_id == test_user.id, Notification.type == "low_stock"
            )
            .first()
        )
        assert notif is not None
        assert "Low Stock Item" in notif.message

    def test_generate_low_stock_no_duplicates(self, db, test_user):
        """Test that low stock notifications aren't duplicated"""
        item = InventoryItem(
            item_name="Test Item",
            quantity=Decimal("1"),
            unit="pcs",
            category="other",
            threshold=Decimal("10"),
        )
        db.add(item)
        db.commit()

        # Generate twice
        count1 = NotificationService.generate_low_stock_notifications(db)
        count2 = NotificationService.generate_low_stock_notifications(db)

        # Second run should create 0 (notification already exists)
        assert count2 == 0

    def test_generate_expiring_notifications(self, db, test_user):
        """Test generating expiring item notifications"""
        # Create expiring item
        item = InventoryItem(
            item_name="Expiring Item",
            quantity=Decimal("5"),
            unit="pcs",
            category="other",
            expiration_date=date.today() + timedelta(days=2),
        )
        db.add(item)
        db.commit()

        count = NotificationService.generate_expiring_notifications(
            db, days_threshold=3
        )

        assert count >= 1

        # Check notification created
        notif = (
            db.query(Notification)
            .filter(
                Notification.user_id == test_user.id, Notification.type == "expiring"
            )
            .first()
        )
        assert notif is not None
        assert "Expiring Item" in notif.message

    def test_generate_expiring_notifications_excludes_expired(self, db, test_user):
        """Test that already expired items are excluded"""
        item = InventoryItem(
            item_name="Already Expired",
            quantity=Decimal("5"),
            unit="pcs",
            category="other",
            expiration_date=date.today() - timedelta(days=1),
        )
        db.add(item)
        db.commit()

        count = NotificationService.generate_expiring_notifications(db)

        # Should not create notification for expired item
        notif = (
            db.query(Notification)
            .filter(
                Notification.type == "expiring",
                Notification.message.like("%Already Expired%"),
            )
            .first()
        )
        assert notif is None

    def test_generate_meal_reminders(self, db, test_user, test_recipe):
        """Test generating meal reminders"""
        # Create upcoming meal
        plan = MenuPlan(
            week_start_date=date.today(),
            name="Test Plan",
            created_by=test_user.id,
            is_active=True,
        )
        db.add(plan)
        db.flush()

        meal = PlannedMeal(
            menu_plan_id=plan.id,
            recipe_id=test_recipe.id,
            meal_date=date.today() + timedelta(days=1),
            meal_type="dinner",
            servings_planned=4,
            cooked=False,
        )
        db.add(meal)
        db.commit()

        count = NotificationService.generate_meal_reminders(db, days_ahead=1)

        assert count >= 1

        # Check notification created
        notif = (
            db.query(Notification)
            .filter(
                Notification.user_id == test_user.id,
                Notification.type == "meal_reminder",
            )
            .first()
        )
        assert notif is not None
        assert test_recipe.title in notif.message

    def test_generate_meal_reminders_excludes_cooked(self, db, test_user, test_recipe):
        """Test that meal reminders exclude already cooked meals"""
        plan = MenuPlan(
            week_start_date=date.today(),
            name="Test Plan",
            created_by=test_user.id,
            is_active=True,
        )
        db.add(plan)
        db.flush()

        meal = PlannedMeal(
            menu_plan_id=plan.id,
            recipe_id=test_recipe.id,
            meal_date=date.today(),
            meal_type="dinner",
            servings_planned=4,
            cooked=True,
        )
        db.add(meal)
        db.commit()

        count = NotificationService.generate_meal_reminders(db, days_ahead=0)

        # Should not create notification for cooked meal
        notif = (
            db.query(Notification)
            .filter(
                Notification.type == "meal_reminder",
                Notification.message.like(f"%{test_recipe.title}%"),
            )
            .first()
        )
        assert notif is None

    def test_generate_recipe_update_notification(
        self, db, test_recipe, test_user, admin_user
    ):
        """Test generating recipe update notification"""
        count = NotificationService.generate_recipe_update_notification(
            db, test_recipe.id, test_user.id, 2
        )

        assert count >= 1

        # Check admin got notification (but not the updater)
        admin_notif = (
            db.query(Notification)
            .filter(
                Notification.user_id == admin_user.id,
                Notification.type == "recipe_update",
            )
            .first()
        )
        assert admin_notif is not None

        user_notif = (
            db.query(Notification)
            .filter(
                Notification.user_id == test_user.id,
                Notification.type == "recipe_update",
            )
            .first()
        )
        assert user_notif is None  # Updater should not be notified
