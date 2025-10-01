/**
 * Menu Plan API endpoints
 */

import apiClient from './client';
import {
  MenuPlan,
  MenuPlanCreate,
  MenuPlanUpdate,
  MarkCookedResponse,
} from '../types/menuPlan';

interface MenuPlanListParams {
  week_start?: string;
  active_only?: boolean;
}

interface MenuPlanListResponse {
  menu_plans: MenuPlan[];
}

export const menuPlansApi = {
  /**
   * List menu plans
   */
  list: async (params: MenuPlanListParams = {}): Promise<MenuPlanListResponse> => {
    const response = await apiClient.get<MenuPlanListResponse>('/menu-plans', { params });
    return response.data;
  },

  /**
   * Get menu plan by ID
   */
  getById: async (id: string): Promise<MenuPlan> => {
    const response = await apiClient.get<MenuPlan>(`/menu-plans/${id}`);
    return response.data;
  },

  /**
   * Create menu plan
   */
  create: async (data: MenuPlanCreate): Promise<MenuPlan> => {
    const response = await apiClient.post<MenuPlan>('/menu-plans', data);
    return response.data;
  },

  /**
   * Update menu plan
   */
  update: async (id: string, data: MenuPlanUpdate): Promise<MenuPlan> => {
    const response = await apiClient.put<MenuPlan>(`/menu-plans/${id}`, data);
    return response.data;
  },

  /**
   * Delete menu plan
   */
  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/menu-plans/${id}`);
  },

  /**
   * Mark meal as cooked
   */
  markMealCooked: async (planId: string, mealId: string): Promise<MarkCookedResponse> => {
    const response = await apiClient.post<MarkCookedResponse>(
      `/menu-plans/${planId}/meals/${mealId}/cooked`
    );
    return response.data;
  },
};
