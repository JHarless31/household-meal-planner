"""
Notification Service
Business logic for generating and managing user notifications
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, date, timedelta
from uuid import UUID
import logging

from src.models.notification import Notification
from src.models.inventory import InventoryItem
from src.models.menu_plan import MenuPlan, PlannedMeal
from src.models.recipe import Recipe
from src.models.user import User

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for notification management"""

    @staticmethod
    def create_notification(
        db: Session,
        user_id: UUID,
        notification_type: str,
        title: str,
        message: str,
        link: Optional[str] = None
    ) -> Notification:
        """
        Create a new notification.

        Args:
            db: Database session
            user_id: User ID to notify
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            link: Optional link URL

        Returns:
            Created notification
        """
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
            link=link
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def get_user_notifications(
        db: Session,
        user_id: UUID,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Notification]:
        """
        Get notifications for a user.

        Args:
            db: Database session
            user_id: User ID
            unread_only: Only return unread notifications
            limit: Maximum number of notifications to return

        Returns:
            List of notifications
        """
        query = db.query(Notification).filter(
            Notification.user_id == user_id
        )

        if unread_only:
            query = query.filter(Notification.is_read == False)

        notifications = query.order_by(
            Notification.created_at.desc()
        ).limit(limit).all()

        return notifications

    @staticmethod
    def mark_as_read(
        db: Session,
        notification_id: UUID,
        user_id: UUID
    ) -> Optional[Notification]:
        """
        Mark a notification as read.

        Args:
            db: Database session
            notification_id: Notification ID
            user_id: User ID (for authorization)

        Returns:
            Updated notification or None if not found
        """
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()

        if not notification:
            return None

        notification.is_read = True
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def mark_all_as_read(
        db: Session,
        user_id: UUID
    ) -> int:
        """
        Mark all notifications as read for a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Number of notifications marked as read
        """
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True})

        db.commit()
        return count

    @staticmethod
    def delete_notification(
        db: Session,
        notification_id: UUID,
        user_id: UUID
    ) -> bool:
        """
        Delete a notification.

        Args:
            db: Database session
            notification_id: Notification ID
            user_id: User ID (for authorization)

        Returns:
            True if deleted, False if not found
        """
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()

        if not notification:
            return False

        db.delete(notification)
        db.commit()
        return True

    @staticmethod
    def get_unread_count(
        db: Session,
        user_id: UUID
    ) -> int:
        """
        Get count of unread notifications for a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Count of unread notifications
        """
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()

        return count

    @staticmethod
    def generate_low_stock_notifications(
        db: Session,
        threshold_percentage: float = 0.2
    ) -> int:
        """
        Generate notifications for low stock items.

        Creates notifications for items where quantity <= threshold.

        Args:
            db: Database session
            threshold_percentage: Percentage of threshold to trigger notification

        Returns:
            Number of notifications created
        """
        # Find items at or below threshold
        low_stock_items = db.query(InventoryItem).filter(
            InventoryItem.quantity <= InventoryItem.threshold * threshold_percentage
        ).all()

        # Get all active users to notify
        users = db.query(User).filter(User.is_active == True).all()

        notifications_created = 0

        for item in low_stock_items:
            for user in users:
                # Check if notification already exists for this item
                existing = db.query(Notification).filter(
                    Notification.user_id == user.id,
                    Notification.type == "low_stock",
                    Notification.is_read == False,
                    Notification.message.like(f"%{item.item_name}%")
                ).first()

                if not existing:
                    NotificationService.create_notification(
                        db,
                        user.id,
                        "low_stock",
                        f"Low Stock: {item.item_name}",
                        f"{item.item_name} is running low. Current: {item.quantity} {item.unit or ''}, Threshold: {item.threshold}",
                        f"/inventory"
                    )
                    notifications_created += 1

        return notifications_created

    @staticmethod
    def generate_expiring_notifications(
        db: Session,
        days_threshold: int = 3
    ) -> int:
        """
        Generate notifications for expiring items.

        Creates notifications for items expiring within specified days.

        Args:
            db: Database session
            days_threshold: Number of days before expiration to notify

        Returns:
            Number of notifications created
        """
        expiration_date = date.today() + timedelta(days=days_threshold)

        # Find items expiring soon
        expiring_items = db.query(InventoryItem).filter(
            InventoryItem.expiration_date.isnot(None),
            InventoryItem.expiration_date <= expiration_date,
            InventoryItem.expiration_date >= date.today()
        ).all()

        # Get all active users to notify
        users = db.query(User).filter(User.is_active == True).all()

        notifications_created = 0

        for item in expiring_items:
            days_until_expiry = (item.expiration_date - date.today()).days

            for user in users:
                # Check if notification already exists for this item
                existing = db.query(Notification).filter(
                    Notification.user_id == user.id,
                    Notification.type == "expiring",
                    Notification.is_read == False,
                    Notification.message.like(f"%{item.item_name}%")
                ).first()

                if not existing:
                    urgency = "today" if days_until_expiry == 0 else f"in {days_until_expiry} days"
                    NotificationService.create_notification(
                        db,
                        user.id,
                        "expiring",
                        f"Expiring Soon: {item.item_name}",
                        f"{item.item_name} expires {urgency} ({item.expiration_date.isoformat()}).",
                        f"/inventory"
                    )
                    notifications_created += 1

        return notifications_created

    @staticmethod
    def generate_meal_reminders(
        db: Session,
        days_ahead: int = 1
    ) -> int:
        """
        Generate notifications for upcoming meals.

        Creates reminders for meals planned in the next N days.

        Args:
            db: Database session
            days_ahead: Number of days ahead to remind

        Returns:
            Number of notifications created
        """
        start_date = date.today()
        end_date = start_date + timedelta(days=days_ahead)

        # Find upcoming meals
        upcoming_meals = db.query(PlannedMeal).join(
            MenuPlan, PlannedMeal.menu_plan_id == MenuPlan.id
        ).join(
            Recipe, PlannedMeal.recipe_id == Recipe.id
        ).filter(
            PlannedMeal.meal_date >= start_date,
            PlannedMeal.meal_date <= end_date,
            PlannedMeal.cooked == False,
            MenuPlan.is_active == True
        ).all()

        # Get all active users to notify
        users = db.query(User).filter(User.is_active == True).all()

        notifications_created = 0

        for meal in upcoming_meals:
            recipe = db.query(Recipe).filter(Recipe.id == meal.recipe_id).first()
            if not recipe:
                continue

            days_until_meal = (meal.meal_date - date.today()).days
            timing = "today" if days_until_meal == 0 else f"tomorrow" if days_until_meal == 1 else f"in {days_until_meal} days"

            for user in users:
                # Check if notification already exists for this meal
                existing = db.query(Notification).filter(
                    Notification.user_id == user.id,
                    Notification.type == "meal_reminder",
                    Notification.is_read == False,
                    Notification.message.like(f"%{recipe.title}%"),
                    Notification.message.like(f"%{meal.meal_date}%")
                ).first()

                if not existing:
                    NotificationService.create_notification(
                        db,
                        user.id,
                        "meal_reminder",
                        f"Meal Reminder: {meal.meal_type.title() if meal.meal_type else 'Meal'}",
                        f"{recipe.title} is planned for {meal.meal_type or 'meal'} {timing} ({meal.meal_date.isoformat()}).",
                        f"/menu-plans"
                    )
                    notifications_created += 1

        return notifications_created

    @staticmethod
    def generate_recipe_update_notification(
        db: Session,
        recipe_id: UUID,
        updated_by: UUID,
        version_number: int
    ) -> int:
        """
        Generate notification when a recipe is updated.

        Notifies all users except the one who made the update.

        Args:
            db: Database session
            recipe_id: Recipe that was updated
            updated_by: User who made the update
            version_number: New version number

        Returns:
            Number of notifications created
        """
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            return 0

        # Get all active users except the updater
        users = db.query(User).filter(
            User.is_active == True,
            User.id != updated_by
        ).all()

        notifications_created = 0

        for user in users:
            NotificationService.create_notification(
                db,
                user.id,
                "recipe_update",
                f"Recipe Updated: {recipe.title}",
                f"{recipe.title} has been updated to version {version_number}.",
                f"/recipes/{recipe_id}"
            )
            notifications_created += 1

        return notifications_created
