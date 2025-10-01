/**
 * Rating-related types
 */

export interface Rating {
  id: string;
  recipe_id: string;
  user_id: string;
  rating: boolean; // true = thumbs up, false = thumbs down
  feedback?: string;
  modifications?: string;
  created_at: string;
  updated_at: string;
}

export interface RatingCreate {
  rating: boolean;
  feedback?: string;
  modifications?: string;
}

export interface RatingSummary {
  thumbs_up_count: number;
  thumbs_down_count: number;
  total_ratings: number;
  is_favorite: boolean;
}

export interface RecipeRatingsResponse {
  recipe_id: string;
  ratings: Rating[];
  summary: RatingSummary;
}
