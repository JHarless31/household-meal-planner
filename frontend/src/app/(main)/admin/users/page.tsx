'use client';

import React, { useState, useEffect } from 'react';
import { adminApi } from '@/lib/api/admin';
import { User } from '@/lib/types/user';
import { ProtectedRoute } from '@/components/common/ProtectedRoute';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { Button } from '@/components/common/Button';
import { formatDate, formatRole } from '@/lib/utils/formatters';

export default function AdminUsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const data = await adminApi.listUsers();
      setUsers(data.users);
    } catch (err) {
      setError((err as { message?: string })?.message || 'Failed to load users');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) return <LoadingSpinner size="lg" />;
  if (error) return <ErrorMessage message={error} onRetry={loadUsers} />;

  return (
    <ProtectedRoute requiredRole="admin">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">User Management</h1>
          <Button>Add User</Button>
        </div>

        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Username</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {users.map((user) => (
                <tr key={user.id}>
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">{user.username}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-500">{user.email}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs bg-primary-100 text-primary-800 rounded">
                      {formatRole(user.role)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {user.is_active ? (
                      <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">Active</span>
                    ) : (
                      <span className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded">Inactive</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatDate(user.created_at, 'PP')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </ProtectedRoute>
  );
}
