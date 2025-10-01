/**
 * Shopping List API endpoints
 */

import apiClient from './client';
import { ShoppingList } from '../types/shoppingList';

interface ShoppingListParams {
  grouped?: boolean;
}

export const shoppingListsApi = {
  /**
   * Generate shopping list for menu plan
   */
  generate: async (planId: string, params: ShoppingListParams = {}): Promise<ShoppingList> => {
    const response = await apiClient.get<ShoppingList>(`/shopping-list/${planId}`, { params });
    return response.data;
  },

  /**
   * Mark item as purchased
   */
  markPurchased: async (
    listId: string,
    itemId: string
  ): Promise<{ message: string; inventory_updated: boolean }> => {
    const response = await apiClient.post<{ message: string; inventory_updated: boolean }>(
      `/shopping-list/${listId}/items/${itemId}/check`
    );
    return response.data;
  },
};
