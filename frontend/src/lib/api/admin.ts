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
};
