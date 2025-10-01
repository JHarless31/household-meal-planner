/**
 * Shopping list-related types
 */

export interface ShoppingListItem {
  id: string;
  name: string;
  quantity: number;
  unit?: string;
  category?: string;
  needed_for_recipes: string[]; // Recipe IDs
  in_stock: boolean;
  checked: boolean;
}

export interface ShoppingList {
  menu_plan_id: string;
  items: ShoppingListItem[];
  generated_at: string;
}
