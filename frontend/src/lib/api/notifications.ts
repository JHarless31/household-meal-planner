/**
 * Notifications API Client
 */

import { apiClient } from './client';

export interface Notification {
  id: string;
  type: 'low_stock' | 'expiring' | 'meal_reminder' | 'recipe_update' | 'system';
  title: string;
  message: string;
  link: string | null;
  is_read: boolean;
  created_at: string;
}

export interface NotificationsResponse {
  notifications: Notification[];
  unread_count: number;
  total: number;
}

/**
 * Get notifications for current user
 */
export async function getNotifications(
  unreadOnly: boolean = false,
  limit: number = 50
): Promise<NotificationsResponse> {
  const response = await apiClient.get<NotificationsResponse>('/notifications', {
    params: { unread_only: unreadOnly, limit },
  });
  return response.data;
}

/**
 * Get unread notification count
 */
export async function getUnreadCount(): Promise<number> {
  const response = await apiClient.get<{ unread_count: number }>(
    '/notifications/unread-count'
  );
  return response.data.unread_count;
}

/**
 * Mark notification as read
 */
export async function markNotificationRead(
  notificationId: string
): Promise<Notification> {
  const response = await apiClient.post<Notification>(
    `/notifications/${notificationId}/mark-read`
  );
  return response.data;
}

/**
 * Mark all notifications as read
 */
export async function markAllNotificationsRead(): Promise<{ marked_read: number }> {
  const response = await apiClient.post<{ marked_read: number }>(
    '/notifications/mark-all-read'
  );
  return response.data;
}

/**
 * Delete notification
 */
export async function deleteNotification(notificationId: string): Promise<void> {
  await apiClient.delete(`/notifications/${notificationId}`);
}
