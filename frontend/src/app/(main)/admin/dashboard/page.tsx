/**
 * Admin Dashboard Page
 * Displays system statistics and charts
 */

'use client';

import { useQuery } from '@tanstack/react-query';
import { adminApi } from '@/lib/api/admin';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: '#10b981',
  medium: '#f59e0b',
  hard: '#ef4444',
};

export default function AdminDashboard() {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['admin', 'statistics'],
    queryFn: () => adminApi.getStatistics(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="animate-pulse space-y-8">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="p-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">Failed to load statistics. Please try again.</p>
        </div>
      </div>
    );
  }

  // Prepare difficulty distribution data for pie chart
  const difficultyData = Object.entries(stats.difficulty_distribution).map(([key, value]) => ({
    name: key.charAt(0).toUpperCase() + key.slice(1),
    value,
    color: DIFFICULTY_COLORS[key] || '#6b7280',
  }));

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Admin Dashboard</h1>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <StatCard
          title="Total Users"
          value={stats.totals.users}
          subtitle={`${stats.totals.active_users} active`}
          icon="👥"
          color="blue"
        />
        <StatCard
          title="Total Recipes"
          value={stats.totals.recipes}
          icon="📖"
          color="green"
        />
        <StatCard
          title="Menu Plans"
          value={stats.totals.menu_plans}
          icon="📅"
          color="purple"
        />
        <StatCard
          title="Inventory Items"
          value={stats.totals.inventory_items}
          subtitle={`${stats.totals.low_stock_items} low stock`}
          icon="📦"
          color="orange"
        />
        <StatCard
          title="Active Users"
          value={stats.totals.active_users}
          subtitle="Last 30 days"
          icon="✓"
          color="emerald"
        />
        <StatCard
          title="Low Stock Items"
          value={stats.totals.low_stock_items}
          icon="⚠️"
          color="red"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Most Cooked Recipes */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Most Cooked Recipes</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stats.most_cooked_recipes.slice(0, 10)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="title" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="times_cooked" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Most Favorited Recipes */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Most Favorited Recipes
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stats.most_favorited_recipes.slice(0, 10)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="title" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="avg_rating" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recipe Difficulty Distribution */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Recipe Difficulty Distribution
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={difficultyData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => `${entry.name}: ${entry.value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {difficultyData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Recipes Over Time */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Recipes Created Over Time
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={stats.recipes_over_time}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="month"
                tickFormatter={(value) =>
                  new Date(value).toLocaleDateString('en-US', {
                    month: 'short',
                    year: '2-digit',
                  })
                }
              />
              <YAxis />
              <Tooltip
                labelFormatter={(value) =>
                  new Date(value).toLocaleDateString('en-US', {
                    month: 'long',
                    year: 'numeric',
                  })
                }
              />
              <Legend />
              <Line type="monotone" dataKey="count" stroke="#8b5cf6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-4 text-sm text-gray-500 text-right">
        Last updated: {new Date(stats.generated_at).toLocaleString()}
      </div>
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: number;
  subtitle?: string;
  icon: string;
  color: string;
}

function StatCard({ title, value, subtitle, icon, color }: StatCardProps) {
  const colorClasses: Record<string, string> = {
    blue: 'bg-blue-100 text-blue-800',
    green: 'bg-green-100 text-green-800',
    purple: 'bg-purple-100 text-purple-800',
    orange: 'bg-orange-100 text-orange-800',
    red: 'bg-red-100 text-red-800',
    emerald: 'bg-emerald-100 text-emerald-800',
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value.toLocaleString()}</p>
          {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div
          className={`text-4xl ${
            colorClasses[color] || 'bg-gray-100 text-gray-800'
          } w-16 h-16 rounded-full flex items-center justify-center`}
        >
          {icon}
        </div>
      </div>
    </div>
  );
}
