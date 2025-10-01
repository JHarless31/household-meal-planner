"""Notifications API Routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.user import User
from src.services.notification_service import NotificationService

router = APIRouter()


@router.get("", response_model=dict)
async def get_notifications(
    unread_only: bool = Query(False, description="Only return unread notifications"),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get notifications for the current user.

    Args:
        unread_only: Filter to only unread notifications
        limit: Maximum number of notifications to return

    Returns:
        List of notifications with unread count
    """
    notifications = NotificationService.get_user_notifications(
        db,
        current_user.id,
        unread_only,
        limit
    )

    unread_count = NotificationService.get_unread_count(db, current_user.id)

    return {
        "notifications": [
            {
                "id": str(notif.id),
                "type": notif.type,
                "title": notif.title,
                "message": notif.message,
                "link": notif.link,
                "is_read": notif.is_read,
                "created_at": notif.created_at.isoformat()
            }
            for notif in notifications
        ],
        "unread_count": unread_count,
        "total": len(notifications)
    }


@router.get("/unread-count", response_model=dict)
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get count of unread notifications for the current user."""
    count = NotificationService.get_unread_count(db, current_user.id)
    return {"unread_count": count}


@router.post("/{notificationId}/mark-read", response_model=dict)
async def mark_notification_read(
    notificationId: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark a notification as read.

    Args:
        notificationId: Notification ID to mark as read

    Returns:
        Updated notification
    """
    notification = NotificationService.mark_as_read(db, notificationId, current_user.id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    return {
        "id": str(notification.id),
        "type": notification.type,
        "title": notification.title,
        "message": notification.message,
        "link": notification.link,
        "is_read": notification.is_read,
        "created_at": notification.created_at.isoformat()
    }


@router.post("/mark-all-read", response_model=dict)
async def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read for the current user."""
    count = NotificationService.mark_all_as_read(db, current_user.id)
    return {"marked_read": count}


@router.delete("/{notificationId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notificationId: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a notification."""
    success = NotificationService.delete_notification(db, notificationId, current_user.id)

    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")


@router.post("/generate/low-stock", response_model=dict)
async def generate_low_stock_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate notifications for low stock items.
    Admin or automated task endpoint.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    count = NotificationService.generate_low_stock_notifications(db)
    return {"notifications_created": count}


@router.post("/generate/expiring", response_model=dict)
async def generate_expiring_notifications(
    days: int = Query(3, ge=1, le=14, description="Days ahead to check for expiring items"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate notifications for expiring items.
    Admin or automated task endpoint.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    count = NotificationService.generate_expiring_notifications(db, days)
    return {"notifications_created": count}


@router.post("/generate/meal-reminders", response_model=dict)
async def generate_meal_reminders(
    days: int = Query(1, ge=1, le=7, description="Days ahead to remind for meals"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate meal reminder notifications.
    Admin or automated task endpoint.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    count = NotificationService.generate_meal_reminders(db, days)
    return {"notifications_created": count}
