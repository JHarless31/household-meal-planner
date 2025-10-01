'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { menuPlansApi } from '@/lib/api/menuPlans';
import { useToast } from '@/contexts/ToastContext';
import { Input } from '@/components/common/Input';
import { Button } from '@/components/common/Button';
import { getMondayOfWeek } from '@/lib/utils/helpers';

export default function NewMenuPlanPage() {
  const router = useRouter();
  const { showToast } = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const monday = getMondayOfWeek();
  const [formData, setFormData] = useState({
    week_start_date: monday.toISOString().split('T')[0],
    name: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const menuPlan = await menuPlansApi.create(formData);
      showToast('success', 'Menu plan created successfully!');
      router.push(`/menu-plans/${menuPlan.id}`);
    } catch (error) {
      showToast('error', (error as { message?: string })?.message || 'Failed to create menu plan');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Create Menu Plan</h1>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
        <Input
          label="Plan Name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          placeholder="e.g., Week of Dec 25"
        />
        <Input
          label="Week Start Date (Monday)"
          type="date"
          value={formData.week_start_date}
          onChange={(e) => setFormData({ ...formData, week_start_date: e.target.value })}
          required
          helperText="Must be a Monday"
        />

        <div className="flex justify-end gap-3">
          <Button type="button" variant="ghost" onClick={() => router.back()}>
            Cancel
          </Button>
          <Button type="submit" isLoading={isLoading}>
            Create Menu Plan
          </Button>
        </div>
      </form>
    </div>
  );
}
