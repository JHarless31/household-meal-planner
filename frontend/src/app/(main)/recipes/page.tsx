'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { recipesApi } from '@/lib/api/recipes';
import { RecipeSummary } from '@/lib/types/recipe';
import { RecipeCard } from '@/components/recipes/RecipeCard';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { EmptyState } from '@/components/common/EmptyState';
import { Button } from '@/components/common/Button';
import { Input } from '@/components/common/Input';
import { Select } from '@/components/common/Select';
import { DIFFICULTY_OPTIONS, RECIPE_FILTER_OPTIONS } from '@/lib/utils/constants';

export default function RecipesPage() {
  const [recipes, setRecipes] = useState<RecipeSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [filter, setFilter] = useState('');

  useEffect(() => {
    loadRecipes();
  }, [search, difficulty, filter]);

  const loadRecipes = async () => {
    try {
      const params: Record<string, string> = {};
      if (search) params.search = search;
      if (difficulty) params.difficulty = difficulty;
      if (filter) params.filter = filter;

      const data = await recipesApi.list(params);
      setRecipes(data.recipes);
    } catch (err) {
      setError((err as { message?: string })?.message || 'Failed to load recipes');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) return <LoadingSpinner size="lg" />;
  if (error) return <ErrorMessage message={error} onRetry={loadRecipes} />;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Recipes</h1>
        <Link href="/recipes/new">
          <Button>Add Recipe</Button>
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Input
            placeholder="Search recipes..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <Select
            options={[{ value: '', label: 'All Difficulties' }, ...DIFFICULTY_OPTIONS]}
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          />
          <Select
            options={[{ value: '', label: 'All Recipes' }, ...RECIPE_FILTER_OPTIONS]}
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          />
        </div>
      </div>

      {recipes.length === 0 ? (
        <EmptyState
          title="No recipes found"
          message="Get started by adding your first recipe"
          actionLabel="Add Recipe"
          onAction={() => window.location.href = '/recipes/new'}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recipes.map((recipe) => (
            <RecipeCard key={recipe.id} recipe={recipe} />
          ))}
        </div>
      )}
    </div>
  );
}
