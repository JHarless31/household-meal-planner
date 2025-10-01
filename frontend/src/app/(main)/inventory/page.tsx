'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { inventoryApi } from '@/lib/api/inventory';
import { InventoryItem } from '@/lib/types/inventory';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { EmptyState } from '@/components/common/EmptyState';
import { Button } from '@/components/common/Button';
import { formatDate, daysUntilExpiration } from '@/lib/utils/formatters';

export default function InventoryPage() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadInventory();
  }, []);

  const loadInventory = async () => {
    try {
      const data = await inventoryApi.list();
      setItems(data.items);
    } catch (err) {
      setError((err as { message?: string })?.message || 'Failed to load inventory');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) return <LoadingSpinner size="lg" />;
  if (error) return <ErrorMessage message={error} onRetry={loadInventory} />;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Inventory</h1>
        <Link href="/inventory/new">
          <Button>Add Item</Button>
        </Link>
      </div>

      {items.length === 0 ? (
        <EmptyState
          title="No inventory items"
          message="Start tracking your kitchen inventory"
          actionLabel="Add Item"
          onAction={() => window.location.href = '/inventory/new'}
        />
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Item</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantity</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Expires</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {items.map((item) => {
                const daysLeft = daysUntilExpiration(item.expiration_date);
                const isLowStock = item.minimum_stock && item.quantity <= item.minimum_stock;
                const isExpiringSoon = daysLeft !== null && daysLeft <= 7;

                return (
                  <tr key={item.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Link href={`/inventory/${item.id}`} className="text-primary-600 hover:text-primary-700">
                        {item.item_name}
                      </Link>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {item.quantity} {item.unit}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap capitalize">{item.location}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {item.expiration_date ? formatDate(item.expiration_date, 'PP') : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {isLowStock && (
                        <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded">Low Stock</span>
                      )}
                      {isExpiringSoon && (
                        <span className="px-2 py-1 text-xs bg-red-100 text-red-800 rounded">Expiring Soon</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
