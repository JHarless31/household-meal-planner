/**
 * Recipe Suggestions Component
 * Displays intelligent recipe suggestions based on various strategies
 */

'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getRecipeSuggestions, SuggestionStrategy } from '@/lib/api/suggestions';
import Link from 'next/link';

const STRATEGY_OPTIONS: { value: SuggestionStrategy; label: string; description: string }[] = [
  { value: 'rotation', label: 'Rotation', description: 'Recipes not cooked recently' },
  { value: 'favorites', label: 'Favorites', description: 'Household favorites' },
  { value: 'never_tried', label: 'Never Tried', description: 'New recipes to explore' },
  { value: 'available_inventory', label: 'Available Inventory', description: 'Based on what you have' },
  { value: 'seasonal', label: 'Seasonal', description: 'Perfect for this season' },
  { value: 'quick_meals', label: 'Quick Meals', description: 'Fast recipes under 30 min' },
];

interface RecipeSuggestionsProps {
  defaultStrategy?: SuggestionStrategy;
  limit?: number;
  showStrategySelector?: boolean;
  onRecipeSelect?: (recipeId: string) => void;
}

export default function RecipeSuggestions({
  defaultStrategy = 'rotation',
  limit = 10,
  showStrategySelector = true,
  onRecipeSelect,
}: RecipeSuggestionsProps) {
  const [strategy, setStrategy] = useState<SuggestionStrategy>(defaultStrategy);

  const { data, isLoading, error } = useQuery({
    queryKey: ['recipe-suggestions', strategy, limit],
    queryFn: () => getRecipeSuggestions(strategy, limit),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-700">Failed to load suggestions. Please try again.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Recipe Suggestions</h3>
        {showStrategySelector && (
          <div className="mt-3">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Suggestion Strategy
            </label>
            <select
              value={strategy}
              onChange={(e) => setStrategy(e.target.value as SuggestionStrategy)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {STRATEGY_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label} - {option.description}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      <div className="p-4">
        {isLoading ? (
          <div className="space-y-3">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-100 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        ) : data && data.suggestions.length > 0 ? (
          <div className="space-y-3">
            {data.suggestions.map((suggestion) => (
              <div
                key={suggestion.recipe_id}
                className="p-3 border border-gray-200 rounded-md hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <Link
                      href={`/recipes/${suggestion.recipe_id}`}
                      className="text-base font-medium text-blue-600 hover:text-blue-800"
                    >
                      {suggestion.title}
                    </Link>
                    {suggestion.description && (
                      <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                        {suggestion.description}
                      </p>
                    )}
                    <div className="mt-2 flex flex-wrap gap-2">
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {suggestion.reason}
                      </span>
                      {suggestion.match_percent !== undefined && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {suggestion.match_percent}% ingredients available
                        </span>
                      )}
                      {suggestion.total_time_minutes !== undefined && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                          {suggestion.total_time_minutes} min
                        </span>
                      )}
                      {suggestion.average_rating !== undefined && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                          {suggestion.average_rating.toFixed(1)} stars
                        </span>
                      )}
                    </div>
                  </div>
                  {onRecipeSelect && (
                    <button
                      onClick={() => onRecipeSelect(suggestion.recipe_id)}
                      className="ml-3 px-3 py-1 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      Add
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-4">
            No suggestions available. Try a different strategy!
          </p>
        )}
      </div>
    </div>
  );
}
