/**
 * Inventory API endpoints
 */

import apiClient from './client';
import {
  InventoryItem,
  InventoryItemCreate,
  InventoryItemUpdate,
  InventoryHistoryResponse,
  ExpiringItem,
  InventoryLocation,
} from '../types/inventory';

interface InventoryListParams {
  category?: string;
  location?: InventoryLocation;
  low_stock?: boolean;
}

interface InventoryListResponse {
  items: InventoryItem[];
}

interface LowStockResponse {
  items: InventoryItem[];
}

interface ExpiringItemsParams {
  days?: number;
}

interface ExpiringItemsResponse {
  items: ExpiringItem[];
}

export const inventoryApi = {
  /**
   * List inventory items
   */
  list: async (params: InventoryListParams = {}): Promise<InventoryListResponse> => {
    const response = await apiClient.get<InventoryListResponse>('/inventory', { params });
    return response.data;
  },

  /**
   * Get inventory item by ID
   */
  getById: async (id: string): Promise<InventoryItem> => {
    const response = await apiClient.get<InventoryItem>(`/inventory/${id}`);
    return response.data;
  },

  /**
   * Add inventory item
   */
  create: async (data: InventoryItemCreate): Promise<InventoryItem> => {
    const response = await apiClient.post<InventoryItem>('/inventory', data);
    return response.data;
  },

  /**
   * Update inventory item
   */
  update: async (id: string, data: InventoryItemUpdate): Promise<InventoryItem> => {
    const response = await apiClient.put<InventoryItem>(`/inventory/${id}`, data);
    return response.data;
  },

  /**
   * Delete inventory item
   */
  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/inventory/${id}`);
  },

  /**
   * Get low stock items
   */
  getLowStock: async (): Promise<LowStockResponse> => {
    const response = await apiClient.get<LowStockResponse>('/inventory/low-stock');
    return response.data;
  },

  /**
   * Get expiring items
   */
  getExpiring: async (params: ExpiringItemsParams = {}): Promise<ExpiringItemsResponse> => {
    const response = await apiClient.get<ExpiringItemsResponse>('/inventory/expiring', {
      params,
    });
    return response.data;
  },

  /**
   * Get item history
   */
  getHistory: async (id: string): Promise<InventoryHistoryResponse> => {
    const response = await apiClient.get<InventoryHistoryResponse>(`/inventory/${id}/history`);
    return response.data;
  },
};
