/**
 * Recipe Card component
 */

import React from 'react';
import Link from 'next/link';
import { RecipeSummary } from '@/lib/types/recipe';
import { formatTime, formatRelativeTime } from '@/lib/utils/formatters';

interface RecipeCardProps {
  recipe: RecipeSummary;
}

export const RecipeCard: React.FC<RecipeCardProps> = ({ recipe }) => {
  const totalTime = (recipe.prep_time_minutes || 0) + (recipe.cook_time_minutes || 0);

  return (
    <Link href={`/recipes/${recipe.id}`}>
      <div className="bg-white rounded-lg shadow hover:shadow-md transition-shadow overflow-hidden">
        <div className="p-6">
          <div className="flex items-start justify-between">
            <h3 className="text-lg font-semibold text-gray-900 flex-1">{recipe.title}</h3>
            {recipe.is_favorite && (
              <span className="ml-2 text-yellow-500">
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </span>
            )}
          </div>
          {recipe.description && (
            <p className="mt-2 text-sm text-gray-600 line-clamp-2">{recipe.description}</p>
          )}
          <div className="mt-4 flex flex-wrap gap-2 text-sm text-gray-500">
            {totalTime > 0 && (
              <span className="flex items-center gap-1">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                {formatTime(totalTime)}
              </span>
            )}
            {recipe.difficulty && (
              <span className="capitalize px-2 py-1 bg-gray-100 rounded">{recipe.difficulty}</span>
            )}
            {recipe.servings && <span>{recipe.servings} servings</span>}
          </div>
          {recipe.tags && recipe.tags.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {recipe.tags.slice(0, 3).map((tag) => (
                <span key={tag} className="text-xs px-2 py-1 bg-primary-50 text-primary-700 rounded">
                  {tag}
                </span>
              ))}
            </div>
          )}
          {recipe.last_cooked_date && (
            <p className="mt-3 text-xs text-gray-500">
              Last cooked: {formatRelativeTime(recipe.last_cooked_date)}
            </p>
          )}
        </div>
      </div>
    </Link>
  );
};
