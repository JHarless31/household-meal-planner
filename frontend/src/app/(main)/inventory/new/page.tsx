'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { inventoryApi } from '@/lib/api/inventory';
import { useToast } from '@/contexts/ToastContext';
import { Input } from '@/components/common/Input';
import { Select } from '@/components/common/Select';
import { Button } from '@/components/common/Button';
import { InventoryItemCreate } from '@/lib/types/inventory';
import { INVENTORY_LOCATION_OPTIONS } from '@/lib/utils/constants';

export default function NewInventoryItemPage() {
  const router = useRouter();
  const { showToast } = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState<InventoryItemCreate>({
    item_name: '',
    quantity: 0,
    unit: '',
    category: '',
    location: 'pantry',
    minimum_stock: 0,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await inventoryApi.create(formData);
      showToast('success', 'Item added successfully!');
      router.push('/inventory');
    } catch (error) {
      showToast('error', (error as { message?: string })?.message || 'Failed to add item');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Add Inventory Item</h1>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
        <Input
          label="Item Name"
          value={formData.item_name}
          onChange={(e) => setFormData({ ...formData, item_name: e.target.value })}
          required
        />
        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Quantity"
            type="number"
            value={formData.quantity}
            onChange={(e) => setFormData({ ...formData, quantity: parseFloat(e.target.value) })}
            required
          />
          <Input
            label="Unit"
            value={formData.unit || ''}
            onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Category"
            value={formData.category || ''}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
          />
          <Select
            label="Location"
            options={INVENTORY_LOCATION_OPTIONS}
            value={formData.location || ''}
            onChange={(e) => setFormData({ ...formData, location: e.target.value as 'pantry' | 'fridge' | 'freezer' | 'other' })}
          />
        </div>
        <Input
          label="Minimum Stock"
          type="number"
          value={formData.minimum_stock || ''}
          onChange={(e) => setFormData({ ...formData, minimum_stock: parseFloat(e.target.value) })}
        />
        <Input
          label="Expiration Date"
          type="date"
          value={formData.expiration_date || ''}
          onChange={(e) => setFormData({ ...formData, expiration_date: e.target.value })}
        />

        <div className="flex justify-end gap-3">
          <Button type="button" variant="ghost" onClick={() => router.back()}>
            Cancel
          </Button>
          <Button type="submit" isLoading={isLoading}>
            Add Item
          </Button>
        </div>
      </form>
    </div>
  );
}
