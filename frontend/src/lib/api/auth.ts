/**
 * Authentication API endpoints
 */

import apiClient from './client';
import { User, LoginRequest, LoginResponse, RegisterRequest } from '../types/user';

export const authApi = {
  /**
   * Register a new user
   */
  register: async (data: RegisterRequest): Promise<User> => {
    const response = await apiClient.post<User>('/auth/register', data);
    return response.data;
  },

  /**
   * Login user
   */
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/login', data);
    return response.data;
  },

  /**
   * Logout user
   */
  logout: async (): Promise<{ message: string }> => {
    const response = await apiClient.post<{ message: string }>('/auth/logout');
    return response.data;
  },

  /**
   * Get current user
   */
  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },
};
