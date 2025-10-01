'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { recipesApi } from '@/lib/api/recipes';
import { Recipe } from '@/lib/types/recipe';
import { RatingWidget } from '@/components/ratings/RatingWidget';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { Button } from '@/components/common/Button';
import { ConfirmDialog } from '@/components/common/ConfirmDialog';
import { useToast } from '@/contexts/ToastContext';
import { formatTime, formatQuantity } from '@/lib/utils/formatters';

export default function RecipeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { showToast } = useToast();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    loadRecipe();
  }, [params.id]);

  const loadRecipe = async () => {
    try {
      const data = await recipesApi.getById(params.id as string);
      setRecipe(data);
    } catch (err) {
      setError((err as { message?: string })?.message || 'Failed to load recipe');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await recipesApi.delete(params.id as string);
      showToast('success', 'Recipe deleted successfully');
      router.push('/recipes');
    } catch (error) {
      showToast('error', 'Failed to delete recipe');
      setIsDeleting(false);
    }
  };

  if (isLoading) return <LoadingSpinner size="lg" />;
  if (error) return <ErrorMessage message={error} onRetry={loadRecipe} />;
  if (!recipe) return null;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{recipe.title}</h1>
          {recipe.description && <p className="mt-2 text-gray-600">{recipe.description}</p>}
        </div>
        <div className="flex gap-2">
          <Link href={`/recipes/${recipe.id}/edit`}>
            <Button variant="secondary">Edit</Button>
          </Link>
          <Button variant="danger" onClick={() => setShowDeleteDialog(true)}>
            Delete
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex gap-6 text-sm text-gray-600">
              {recipe.prep_time_minutes && (
                <div>
                  <span className="font-medium">Prep:</span> {formatTime(recipe.prep_time_minutes)}
                </div>
              )}
              {recipe.cook_time_minutes && (
                <div>
                  <span className="font-medium">Cook:</span> {formatTime(recipe.cook_time_minutes)}
                </div>
              )}
              {recipe.servings && (
                <div>
                  <span className="font-medium">Servings:</span> {recipe.servings}
                </div>
              )}
              {recipe.difficulty && (
                <div>
                  <span className="font-medium">Difficulty:</span> {recipe.difficulty}
                </div>
              )}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Ingredients</h2>
            <ul className="space-y-2">
              {recipe.ingredients.map((ingredient) => (
                <li key={ingredient.id} className="flex items-start">
                  <span className="mr-2 text-primary-600">•</span>
                  <span>
                    {formatQuantity(ingredient.quantity, ingredient.unit)} {ingredient.name}
                    {ingredient.is_optional && (
                      <span className="ml-2 text-sm text-gray-500">(optional)</span>
                    )}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Instructions</h2>
            <div className="prose max-w-none">
              <p className="whitespace-pre-wrap">{recipe.instructions}</p>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <RatingWidget recipeId={recipe.id} />

          {recipe.tags && recipe.tags.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="font-semibold text-gray-900 mb-3">Tags</h3>
              <div className="flex flex-wrap gap-2">
                {recipe.tags.map((tag) => (
                  <span key={tag} className="px-3 py-1 bg-primary-50 text-primary-700 rounded-full text-sm">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <ConfirmDialog
        isOpen={showDeleteDialog}
        onClose={() => setShowDeleteDialog(false)}
        onConfirm={handleDelete}
        title="Delete Recipe"
        message="Are you sure you want to delete this recipe? This action cannot be undone."
        confirmText="Delete"
        isLoading={isDeleting}
      />
    </div>
  );
}
