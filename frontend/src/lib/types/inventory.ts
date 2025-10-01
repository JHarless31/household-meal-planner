/**
 * Inventory-related types
 */

export type InventoryLocation = 'pantry' | 'fridge' | 'freezer' | 'other';
export type ChangeType = 'purchased' | 'used' | 'expired' | 'adjusted' | 'auto_deducted';

export interface InventoryItem {
  id: string;
  item_name: string;
  quantity: number;
  unit?: string;
  category?: string;
  location?: InventoryLocation;
  expiration_date?: string;
  minimum_stock?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface InventoryItemCreate {
  item_name: string;
  quantity: number;
  unit?: string;
  category?: string;
  location?: InventoryLocation;
  expiration_date?: string;
  minimum_stock?: number;
  notes?: string;
}

export interface InventoryItemUpdate {
  item_name?: string;
  quantity?: number;
  unit?: string;
  category?: string;
  location?: InventoryLocation;
  expiration_date?: string;
  minimum_stock?: number;
  notes?: string;
}

export interface InventoryHistory {
  id: string;
  change_type: ChangeType;
  quantity_before: number;
  quantity_after: number;
  quantity_change: number;
  reason?: string;
  changed_by: string;
  changed_at: string;
}

export interface InventoryHistoryResponse {
  item_id: string;
  history: InventoryHistory[];
}

export interface ExpiringItem extends InventoryItem {
  days_until_expiration: number;
}
