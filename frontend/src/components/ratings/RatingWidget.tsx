'use client';

/**
 * Rating Widget component
 */

import React, { useState, useEffect } from 'react';
import { ratingsApi } from '@/lib/api/ratings';
import { useAuth } from '@/contexts/AuthContext';
import { useToast } from '@/contexts/ToastContext';
import { RecipeRatingsResponse } from '@/lib/types/rating';
import { formatRatingPercentage } from '@/lib/utils/formatters';

interface RatingWidgetProps {
  recipeId: string;
}

export const RatingWidget: React.FC<RatingWidgetProps> = ({ recipeId }) => {
  const { user } = useAuth();
  const { showToast } = useToast();
  const [ratings, setRatings] = useState<RecipeRatingsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadRatings();
  }, [recipeId]);

  const loadRatings = async () => {
    try {
      const data = await ratingsApi.getRecipeRatings(recipeId);
      setRatings(data);
    } catch (error) {
      console.error('Failed to load ratings', error);
    }
  };

  const handleRate = async (thumbsUp: boolean) => {
    if (!user) return;

    setIsLoading(true);
    try {
      const userRating = ratings?.ratings.find((r) => r.user_id === user.id);

      if (userRating) {
        // Update existing rating
        await ratingsApi.updateRating(recipeId, userRating.id, { rating: thumbsUp });
      } else {
        // Create new rating
        await ratingsApi.rateRecipe(recipeId, { rating: thumbsUp });
      }

      await loadRatings();
      showToast('success', 'Rating saved!');
    } catch (error) {
      showToast('error', 'Failed to save rating');
    } finally {
      setIsLoading(false);
    }
  };

  if (!ratings) return null;

  const userRating = ratings.ratings.find((r) => r.user_id === user?.id);
  const percentage = formatRatingPercentage(
    ratings.summary.thumbs_up_count,
    ratings.summary.total_ratings
  );

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <h3 className="font-semibold text-gray-900 mb-3">Rate this recipe</h3>

      <div className="flex items-center gap-4">
        <button
          onClick={() => handleRate(true)}
          disabled={isLoading}
          className={`p-2 rounded-lg transition-colors ${
            userRating?.rating === true
              ? 'bg-green-100 text-green-600'
              : 'hover:bg-gray-100 text-gray-400'
          }`}
          aria-label="Thumbs up"
        >
          <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
          </svg>
        </button>

        <button
          onClick={() => handleRate(false)}
          disabled={isLoading}
          className={`p-2 rounded-lg transition-colors ${
            userRating?.rating === false
              ? 'bg-red-100 text-red-600'
              : 'hover:bg-gray-100 text-gray-400'
          }`}
          aria-label="Thumbs down"
        >
          <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
            <path d="M18 9.5a1.5 1.5 0 11-3 0v-6a1.5 1.5 0 013 0v6zM14 9.667v-5.43a2 2 0 00-1.105-1.79l-.05-.025A4 4 0 0011.055 2H5.64a2 2 0 00-1.962 1.608l-1.2 6A2 2 0 004.44 12H8v4a2 2 0 002 2 1 1 0 001-1v-.667a4 4 0 01.8-2.4l1.4-1.866a4 4 0 00.8-2.4z" />
          </svg>
        </button>

        <div className="flex-1 text-sm">
          <p className="text-gray-700">
            <span className="font-semibold">{percentage}</span> positive (
            {ratings.summary.total_ratings} {ratings.summary.total_ratings === 1 ? 'rating' : 'ratings'})
          </p>
        </div>
      </div>
    </div>
  );
};
