/**
 * Menu planning-related types
 */

import { RecipeSummary } from './recipe';

export type MealType = 'breakfast' | 'lunch' | 'dinner' | 'snack';

export interface PlannedMeal {
  id: string;
  recipe: RecipeSummary;
  meal_date: string;
  meal_type: MealType;
  servings_planned?: number;
  notes?: string;
  cooked: boolean;
  cooked_date?: string;
  cooked_by?: string;
}

export interface PlannedMealInput {
  recipe_id: string;
  meal_date: string;
  meal_type: MealType;
  servings_planned?: number;
  notes?: string;
}

export interface MenuPlan {
  id: string;
  week_start_date: string;
  week_end_date: string;
  name?: string;
  meals: PlannedMeal[];
  created_by: string;
  is_active: boolean;
  created_at: string;
}

export interface MenuPlanCreate {
  week_start_date: string; // Must be a Monday
  name?: string;
}

export interface MenuPlanUpdate {
  name?: string;
  is_active?: boolean;
  meals?: PlannedMealInput[];
}

export interface InventoryChange {
  item_name: string;
  quantity_deducted: number;
}

export interface MarkCookedResponse {
  meal: PlannedMeal;
  inventory_changes: InventoryChange[];
}
