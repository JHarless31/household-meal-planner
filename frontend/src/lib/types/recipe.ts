/**
 * Recipe-related types
 */

export type Difficulty = 'easy' | 'medium' | 'hard';
export type SourceType = 'manual' | 'scraped';

export interface Ingredient {
  id: string;
  name: string;
  quantity?: number;
  unit?: string;
  category?: string;
  is_optional?: boolean;
}

export interface IngredientInput {
  name: string;
  quantity?: number;
  unit?: string;
  category?: string;
  is_optional?: boolean;
}

export interface RecipeSummary {
  id: string;
  title: string;
  description?: string;
  prep_time_minutes?: number;
  cook_time_minutes?: number;
  servings?: number;
  difficulty?: Difficulty;
  tags?: string[];
  is_favorite?: boolean;
  last_cooked_date?: string;
}

export interface Recipe extends RecipeSummary {
  source_url?: string;
  source_type?: SourceType;
  current_version: number;
  ingredients: Ingredient[];
  instructions: string;
  images?: string[];
  nutritional_info?: Record<string, unknown>;
  created_by: string;
  created_at: string;
}

export interface RecipeCreate {
  title: string;
  description?: string;
  prep_time_minutes?: number;
  cook_time_minutes?: number;
  servings?: number;
  difficulty?: Difficulty;
  ingredients: IngredientInput[];
  instructions: string;
  tags?: string[];
  source_url?: string;
}

export interface RecipeUpdate extends RecipeCreate {
  change_description?: string;
}

export interface RecipeVersion {
  version_number: number;
  prep_time_minutes?: number;
  cook_time_minutes?: number;
  servings?: number;
  difficulty?: Difficulty;
  ingredients: Ingredient[];
  instructions: string;
  change_description?: string;
  modified_by: string;
  created_at: string;
}

export interface RecipeVersionsResponse {
  recipe_id: string;
  current_version: number;
  versions: RecipeVersion[];
}

export interface ScrapeRecipeRequest {
  url: string;
}

export interface ScrapeRecipeResponse {
  scraped_data: RecipeCreate;
  source_url: string;
  warnings?: string[];
}

export interface RecipeSuggestion {
  recipe: RecipeSummary;
  score: number;
  reasons: string[];
}

export interface RecipeSuggestionsResponse {
  suggestions: RecipeSuggestion[];
}

export type RecipeFilter = 'favorites' | 'not_recent' | 'never_tried' | 'available_inventory';
