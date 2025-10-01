/**
 * Recipe API endpoints
 */

import apiClient from './client';
import {
  Recipe,
  RecipeSummary,
  RecipeCreate,
  RecipeUpdate,
  RecipeVersionsResponse,
  ScrapeRecipeRequest,
  ScrapeRecipeResponse,
  RecipeSuggestionsResponse,
  RecipeFilter,
  Difficulty,
} from '../types/recipe';
import { Pagination } from '../types/api';

interface RecipeListParams {
  page?: number;
  limit?: number;
  search?: string;
  tags?: string;
  difficulty?: Difficulty;
  filter?: RecipeFilter;
}

interface RecipeListResponse {
  recipes: RecipeSummary[];
  pagination: Pagination;
}

export const recipesApi = {
  /**
   * List recipes with filters
   */
  list: async (params: RecipeListParams = {}): Promise<RecipeListResponse> => {
    const response = await apiClient.get<RecipeListResponse>('/recipes', { params });
    return response.data;
  },

  /**
   * Get recipe by ID
   */
  getById: async (id: string): Promise<Recipe> => {
    const response = await apiClient.get<Recipe>(`/recipes/${id}`);
    return response.data;
  },

  /**
   * Create new recipe
   */
  create: async (data: RecipeCreate): Promise<Recipe> => {
    const response = await apiClient.post<Recipe>('/recipes', data);
    return response.data;
  },

  /**
   * Update recipe (creates new version)
   */
  update: async (id: string, data: RecipeUpdate): Promise<Recipe> => {
    const response = await apiClient.put<Recipe>(`/recipes/${id}`, data);
    return response.data;
  },

  /**
   * Delete recipe
   */
  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/recipes/${id}`);
  },

  /**
   * Get recipe versions
   */
  getVersions: async (id: string): Promise<RecipeVersionsResponse> => {
    const response = await apiClient.get<RecipeVersionsResponse>(`/recipes/${id}/versions`);
    return response.data;
  },

  /**
   * Get specific version
   */
  getVersion: async (id: string, version: number): Promise<Recipe> => {
    const response = await apiClient.get<Recipe>(`/recipes/${id}/versions/${version}`);
    return response.data;
  },

  /**
   * Revert to version
   */
  revertToVersion: async (id: string, version: number): Promise<Recipe> => {
    const response = await apiClient.put<Recipe>(`/recipes/${id}/revert/${version}`);
    return response.data;
  },

  /**
   * Scrape recipe from URL
   */
  scrape: async (data: ScrapeRecipeRequest): Promise<ScrapeRecipeResponse> => {
    const response = await apiClient.post<ScrapeRecipeResponse>('/recipes/scrape', data);
    return response.data;
  },

  /**
   * Get recipe suggestions
   */
  getSuggestions: async (): Promise<RecipeSuggestionsResponse> => {
    const response = await apiClient.get<RecipeSuggestionsResponse>('/recipes/suggestions');
    return response.data;
  },
};
