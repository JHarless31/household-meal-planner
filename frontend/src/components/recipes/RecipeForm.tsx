'use client';

import React, { useState } from 'react';
import { Input } from '@/components/common/Input';
import { Textarea } from '@/components/common/Textarea';
import { Select } from '@/components/common/Select';
import { Button } from '@/components/common/Button';
import { DIFFICULTY_OPTIONS, COMMON_UNITS } from '@/lib/utils/constants';
import { RecipeCreate, IngredientInput } from '@/lib/types/recipe';

interface RecipeFormProps {
  initialData?: Partial<RecipeCreate>;
  onSubmit: (data: RecipeCreate) => Promise<void>;
  isLoading?: boolean;
}

export const RecipeForm: React.FC<RecipeFormProps> = ({ initialData, onSubmit, isLoading }) => {
  const [formData, setFormData] = useState<RecipeCreate>({
    title: initialData?.title || '',
    description: initialData?.description || '',
    prep_time_minutes: initialData?.prep_time_minutes || 0,
    cook_time_minutes: initialData?.cook_time_minutes || 0,
    servings: initialData?.servings || 4,
    difficulty: initialData?.difficulty || 'medium',
    ingredients: initialData?.ingredients || [{ name: '', quantity: 0, unit: '' }],
    instructions: initialData?.instructions || '',
    tags: initialData?.tags || [],
    source_url: initialData?.source_url || '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleIngredientChange = (index: number, field: keyof IngredientInput, value: string | number) => {
    const newIngredients = [...formData.ingredients];
    newIngredients[index] = { ...newIngredients[index], [field]: value };
    setFormData({ ...formData, ingredients: newIngredients });
  };

  const addIngredient = () => {
    setFormData({
      ...formData,
      ingredients: [...formData.ingredients, { name: '', quantity: 0, unit: '' }],
    });
  };

  const removeIngredient = (index: number) => {
    setFormData({
      ...formData,
      ingredients: formData.ingredients.filter((_, i) => i !== index),
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Basic Information</h2>
        <Input
          label="Title"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          error={errors.title}
          required
        />
        <Textarea
          label="Description"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          rows={3}
        />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Input
            label="Prep Time (min)"
            type="number"
            value={formData.prep_time_minutes || ''}
            onChange={(e) => setFormData({ ...formData, prep_time_minutes: parseInt(e.target.value) || 0 })}
          />
          <Input
            label="Cook Time (min)"
            type="number"
            value={formData.cook_time_minutes || ''}
            onChange={(e) => setFormData({ ...formData, cook_time_minutes: parseInt(e.target.value) || 0 })}
          />
          <Input
            label="Servings"
            type="number"
            value={formData.servings || ''}
            onChange={(e) => setFormData({ ...formData, servings: parseInt(e.target.value) || 0 })}
          />
          <Select
            label="Difficulty"
            options={DIFFICULTY_OPTIONS}
            value={formData.difficulty || ''}
            onChange={(e) => setFormData({ ...formData, difficulty: e.target.value as 'easy' | 'medium' | 'hard' })}
          />
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-900">Ingredients</h2>
          <Button type="button" variant="secondary" size="sm" onClick={addIngredient}>
            Add Ingredient
          </Button>
        </div>
        <div className="space-y-3">
          {formData.ingredients.map((ingredient, index) => (
            <div key={index} className="flex gap-2">
              <Input
                placeholder="Ingredient name"
                value={ingredient.name}
                onChange={(e) => handleIngredientChange(index, 'name', e.target.value)}
                className="flex-1"
              />
              <Input
                placeholder="Qty"
                type="number"
                value={ingredient.quantity || ''}
                onChange={(e) => handleIngredientChange(index, 'quantity', parseFloat(e.target.value) || 0)}
                className="w-24"
              />
              <select
                value={ingredient.unit || ''}
                onChange={(e) => handleIngredientChange(index, 'unit', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg w-32"
              >
                <option value="">Unit</option>
                {COMMON_UNITS.map((unit) => (
                  <option key={unit} value={unit}>{unit}</option>
                ))}
              </select>
              <button
                type="button"
                onClick={() => removeIngredient(index)}
                className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Instructions</h2>
        <Textarea
          value={formData.instructions}
          onChange={(e) => setFormData({ ...formData, instructions: e.target.value })}
          rows={8}
          required
        />
      </div>

      <div className="flex justify-end gap-3">
        <Button type="button" variant="ghost" onClick={() => window.history.back()}>
          Cancel
        </Button>
        <Button type="submit" isLoading={isLoading}>
          Save Recipe
        </Button>
      </div>
    </form>
  );
};
