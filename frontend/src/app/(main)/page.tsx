'use client';

/**
 * Dashboard page
 */

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { recipesApi } from '@/lib/api/recipes';
import { inventoryApi } from '@/lib/api/inventory';
import { menuPlansApi } from '@/lib/api/menuPlans';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { Button } from '@/components/common/Button';
import { formatRelativeTime } from '@/lib/utils/formatters';

export default function DashboardPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState({
    totalRecipes: 0,
    activeMenuPlans: 0,
    lowStockItems: 0,
    expiringItems: 0,
  });
  const [recentRecipes, setRecentRecipes] = useState<unknown[]>([]);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const [recipesData, lowStockData, expiringData, menuPlansData] = await Promise.all([
          recipesApi.list({ limit: 5 }),
          inventoryApi.getLowStock(),
          inventoryApi.getExpiring({ days: 7 }),
          menuPlansApi.list({ active_only: true }),
        ]);

        setStats({
          totalRecipes: recipesData.pagination.total_items,
          activeMenuPlans: menuPlansData.menu_plans.length,
          lowStockItems: lowStockData.items.length,
          expiringItems: expiringData.items.length,
        });

        setRecentRecipes(recipesData.recipes);
      } catch (err) {
        setError((err as { message?: string })?.message || 'Failed to load dashboard data');
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  if (isLoading) {
    return <LoadingSpinner size="lg" />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={() => window.location.reload()} />;
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">Welcome to your meal planning dashboard</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Recipes"
          value={stats.totalRecipes}
          icon={
            <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
              />
            </svg>
          }
          href="/recipes"
        />
        <StatCard
          title="Active Menu Plans"
          value={stats.activeMenuPlans}
          icon={
            <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
          }
          href="/menu-plans"
        />
        <StatCard
          title="Low Stock Items"
          value={stats.lowStockItems}
          icon={
            <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          }
          href="/inventory"
          warning={stats.lowStockItems > 0}
        />
        <StatCard
          title="Expiring Soon"
          value={stats.expiringItems}
          icon={
            <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          }
          href="/inventory"
          warning={stats.expiringItems > 0}
        />
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="flex flex-wrap gap-3">
          <Link href="/recipes/new">
            <Button>Add Recipe</Button>
          </Link>
          <Link href="/inventory/new">
            <Button variant="secondary">Add Inventory Item</Button>
          </Link>
          <Link href="/menu-plans/new">
            <Button variant="secondary">Create Menu Plan</Button>
          </Link>
        </div>
      </div>
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  href: string;
  warning?: boolean;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, href, warning }) => {
  return (
    <Link href={href}>
      <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <p
              className={`text-3xl font-bold mt-2 ${
                warning ? 'text-yellow-600' : 'text-gray-900'
              }`}
            >
              {value}
            </p>
          </div>
          <div className={warning ? 'text-yellow-600' : 'text-primary-600'}>{icon}</div>
        </div>
      </div>
    </Link>
  );
};
