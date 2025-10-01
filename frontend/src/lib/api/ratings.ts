/**
 * Rating API endpoints
 */

import apiClient from './client';
import { Rating, RatingCreate, RecipeRatingsResponse } from '../types/rating';

export const ratingsApi = {
  /**
   * Get recipe ratings
   */
  getRecipeRatings: async (recipeId: string): Promise<RecipeRatingsResponse> => {
    const response = await apiClient.get<RecipeRatingsResponse>(`/recipes/${recipeId}/ratings`);
    return response.data;
  },

  /**
   * Rate recipe
   */
  rateRecipe: async (recipeId: string, data: RatingCreate): Promise<Rating> => {
    const response = await apiClient.post<Rating>(`/recipes/${recipeId}/ratings`, data);
    return response.data;
  },

  /**
   * Update rating
   */
  updateRating: async (recipeId: string, ratingId: string, data: RatingCreate): Promise<Rating> => {
    const response = await apiClient.put<Rating>(
      `/recipes/${recipeId}/ratings/${ratingId}`,
      data
    );
    return response.data;
  },

  /**
   * Delete rating
   */
  deleteRating: async (recipeId: string, ratingId: string): Promise<void> => {
    await apiClient.delete(`/recipes/${recipeId}/ratings/${ratingId}`);
  },
};
