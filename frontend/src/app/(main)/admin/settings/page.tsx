'use client';

import React, { useState, useEffect } from 'react';
import { adminApi } from '@/lib/api/admin';
import { AppSettings } from '@/lib/types/admin';
import { ProtectedRoute } from '@/components/common/ProtectedRoute';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { Button } from '@/components/common/Button';
import { Input } from '@/components/common/Input';
import { useToast } from '@/contexts/ToastContext';

export default function AdminSettingsPage() {
  const { showToast } = useToast();
  const [settings, setSettings] = useState<AppSettings | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await adminApi.getSettings();
      setSettings(data);
    } catch (err) {
      setError((err as { message?: string })?.message || 'Failed to load settings');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!settings) return;

    setIsSaving(true);
    try {
      await adminApi.updateSettings(settings);
      showToast('success', 'Settings updated successfully');
    } catch (error) {
      showToast('error', 'Failed to update settings');
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) return <LoadingSpinner size="lg" />;
  if (error) return <ErrorMessage message={error} onRetry={loadSettings} />;
  if (!settings) return null;

  return (
    <ProtectedRoute requiredRole="admin">
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">Application Settings</h1>

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-6">
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Favorites Configuration</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Favorites Threshold (%)"
                type="number"
                min="0"
                max="100"
                value={settings.favorites_threshold * 100}
                onChange={(e) =>
                  setSettings({
                    ...settings,
                    favorites_threshold: parseFloat(e.target.value) / 100,
                  })
                }
                helperText="Percentage of thumbs up required for favorite status"
              />
              <Input
                label="Minimum Raters"
                type="number"
                min="1"
                value={settings.favorites_min_raters}
                onChange={(e) =>
                  setSettings({
                    ...settings,
                    favorites_min_raters: parseInt(e.target.value),
                  })
                }
                helperText="Minimum number of ratings required"
              />
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Inventory Settings</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Low Stock Threshold (%)"
                type="number"
                min="0"
                max="100"
                value={settings.low_stock_threshold_percent * 100}
                onChange={(e) =>
                  setSettings({
                    ...settings,
                    low_stock_threshold_percent: parseFloat(e.target.value) / 100,
                  })
                }
                helperText="Percentage of minimum stock for alerts"
              />
              <Input
                label="Expiration Warning (days)"
                type="number"
                min="0"
                value={settings.expiration_warning_days}
                onChange={(e) =>
                  setSettings({
                    ...settings,
                    expiration_warning_days: parseInt(e.target.value),
                  })
                }
                helperText="Days before expiration to show warning"
              />
            </div>
          </div>

          <div className="flex justify-end gap-3">
            <Button type="button" variant="ghost" onClick={loadSettings}>
              Reset
            </Button>
            <Button type="submit" isLoading={isSaving}>
              Save Settings
            </Button>
          </div>
        </form>
      </div>
    </ProtectedRoute>
  );
}
