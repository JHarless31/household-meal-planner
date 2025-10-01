/**
 * Application constants
 */

export const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME || 'Meal Planning App';
export const APP_VERSION = process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0';

export const DIFFICULTY_OPTIONS = [
  { value: 'easy', label: 'Easy' },
  { value: 'medium', label: 'Medium' },
  { value: 'hard', label: 'Hard' },
] as const;

export const MEAL_TYPE_OPTIONS = [
  { value: 'breakfast', label: 'Breakfast' },
  { value: 'lunch', label: 'Lunch' },
  { value: 'dinner', label: 'Dinner' },
  { value: 'snack', label: 'Snack' },
] as const;

export const INVENTORY_LOCATION_OPTIONS = [
  { value: 'pantry', label: 'Pantry' },
  { value: 'fridge', label: 'Fridge' },
  { value: 'freezer', label: 'Freezer' },
  { value: 'other', label: 'Other' },
] as const;

export const RECIPE_FILTER_OPTIONS = [
  { value: 'favorites', label: 'Favorites' },
  { value: 'not_recent', label: 'Not Recently Cooked' },
  { value: 'never_tried', label: 'Never Tried' },
  { value: 'available_inventory', label: 'Available from Inventory' },
] as const;

export const COMMON_UNITS = [
  'cup',
  'cups',
  'tbsp',
  'tsp',
  'oz',
  'lb',
  'g',
  'kg',
  'ml',
  'l',
  'piece',
  'pieces',
  'whole',
  'to taste',
] as const;

export const COMMON_CATEGORIES = [
  'Produce',
  'Dairy',
  'Meat & Seafood',
  'Grains & Pasta',
  'Canned Goods',
  'Frozen Foods',
  'Spices & Seasonings',
  'Baking',
  'Beverages',
  'Snacks',
  'Other',
] as const;

export const PAGINATION_LIMITS = [10, 20, 50, 100] as const;

export const DEFAULT_PAGE_LIMIT = 20;
