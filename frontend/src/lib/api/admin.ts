/**
 * Admin API endpoints
 */

import apiClient from './client';
import { User, UserCreate, UserUpdate } from '../types/user';
import { AppSettings } from '../types/admin';

interface UsersListResponse {
  users: User[];
}

export const adminApi = {
  /**
   * List all users
   */
  listUsers: async (): Promise<UsersListResponse> => {
    const response = await apiClient.get<UsersListResponse>('/admin/users');
    return response.data;
  },

  /**
   * Create user
   */
  createUser: async (data: UserCreate): Promise<User> => {
    const response = await apiClient.post<User>('/admin/users', data);
    return response.data;
  },

  /**
   * Update user
   */
  updateUser: async (userId: string, data: UserUpdate): Promise<User> => {
    const response = await apiClient.put<User>(`/admin/users/${userId}`, data);
    return response.data;
  },

  /**
   * Delete user
   */
  deleteUser: async (userId: string): Promise<void> => {
    await apiClient.delete(`/admin/users/${userId}`);
  },

  /**
   * Get app settings
   */
  getSettings: async (): Promise<AppSettings> => {
    const response = await apiClient.get<AppSettings>('/admin/settings');
    return response.data;
  },

  /**
   * Update app settings
   */
  updateSettings: async (data: AppSettings): Promise<AppSettings> => {
    const response = await apiClient.put<AppSettings>('/admin/settings', data);
    return response.data;
  },

  /**
   * Get system statistics
   */
  getStatistics: async (): Promise<SystemStatistics> => {
    const response = await apiClient.get<SystemStatistics>('/admin/statistics');
    return response.data;
  },
};

export interface SystemStatistics {
  totals: {
    users: number;
    recipes: number;
    menu_plans: number;
    inventory_items: number;
    active_users: number;
    low_stock_items: number;
  };
  most_cooked_recipes: Array<{
    recipe_id: string;
    title: string;
    times_cooked: number;
  }>;
  most_favorited_recipes: Array<{
    recipe_id: string;
    title: string;
    avg_rating: number;
    rating_count: number;
  }>;
  difficulty_distribution: Record<string, number>;
  recipes_over_time: Array<{
    month: string;
    count: number;
  }>;
  generated_at: string;
}
