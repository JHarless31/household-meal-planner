'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { menuPlansApi } from '@/lib/api/menuPlans';
import { MenuPlan } from '@/lib/types/menuPlan';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { EmptyState } from '@/components/common/EmptyState';
import { Button } from '@/components/common/Button';
import { formatDate } from '@/lib/utils/formatters';

export default function MenuPlansPage() {
  const [menuPlans, setMenuPlans] = useState<MenuPlan[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadMenuPlans();
  }, []);

  const loadMenuPlans = async () => {
    try {
      const data = await menuPlansApi.list({ active_only: true });
      setMenuPlans(data.menu_plans);
    } catch (err) {
      setError((err as { message?: string })?.message || 'Failed to load menu plans');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) return <LoadingSpinner size="lg" />;
  if (error) return <ErrorMessage message={error} onRetry={loadMenuPlans} />;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Menu Plans</h1>
        <Link href="/menu-plans/new">
          <Button>Create Menu Plan</Button>
        </Link>
      </div>

      {menuPlans.length === 0 ? (
        <EmptyState
          title="No menu plans"
          message="Create a menu plan to organize your weekly meals"
          actionLabel="Create Menu Plan"
          onAction={() => window.location.href = '/menu-plans/new'}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {menuPlans.map((plan) => (
            <Link key={plan.id} href={`/menu-plans/${plan.id}`}>
              <div className="bg-white rounded-lg shadow hover:shadow-md transition-shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900">{plan.name || 'Menu Plan'}</h3>
                <p className="mt-2 text-sm text-gray-600">
                  {formatDate(plan.week_start_date, 'PP')} - {formatDate(plan.week_end_date, 'PP')}
                </p>
                <p className="mt-1 text-sm text-gray-500">{plan.meals.length} meals planned</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
