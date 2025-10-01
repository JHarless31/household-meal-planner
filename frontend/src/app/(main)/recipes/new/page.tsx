'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { recipesApi } from '@/lib/api/recipes';
import { useToast } from '@/contexts/ToastContext';
import { RecipeForm } from '@/components/recipes/RecipeForm';
import { RecipeCreate } from '@/lib/types/recipe';

export default function NewRecipePage() {
  const router = useRouter();
  const { showToast } = useToast();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (data: RecipeCreate) => {
    setIsLoading(true);
    try {
      const recipe = await recipesApi.create(data);
      showToast('success', 'Recipe created successfully!');
      router.push(`/recipes/${recipe.id}`);
    } catch (error) {
      showToast('error', (error as { message?: string })?.message || 'Failed to create recipe');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Create New Recipe</h1>
      <RecipeForm onSubmit={handleSubmit} isLoading={isLoading} />
    </div>
  );
}
