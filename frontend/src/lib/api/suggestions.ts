/**
 * Recipe Suggestions API Client
 */

import { apiClient } from './client';

export interface RecipeSuggestion {
  recipe_id: string;
  title: string;
  description: string;
  reason: string;
  strategy: string;
  // Strategy-specific fields
  times_cooked?: number;
  last_cooked_date?: string;
  days_since_cooked?: number;
  average_rating?: number;
  rating_count?: number;
  match_percent?: number;
  matched_ingredients?: number;
  total_ingredients?: number;
  missing_ingredients?: string[];
  season?: string;
  prep_time_minutes?: number;
  cook_time_minutes?: number;
  total_time_minutes?: number;
}

export interface SuggestionsResponse {
  suggestions: RecipeSuggestion[];
  strategy: string;
  count: number;
}

export type SuggestionStrategy =
  | 'rotation'
  | 'favorites'
  | 'never_tried'
  | 'available_inventory'
  | 'seasonal'
  | 'quick_meals';

/**
 * Get recipe suggestions based on strategy
 */
export async function getRecipeSuggestions(
  strategy: SuggestionStrategy = 'rotation',
  limit: number = 10
): Promise<SuggestionsResponse> {
  const response = await apiClient.get<SuggestionsResponse>(
    `/recipes/suggestions`,
    {
      params: { strategy, limit },
    }
  );
  return response.data;
}
