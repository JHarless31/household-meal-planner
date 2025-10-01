'use client';

/**
 * Protected Route wrapper component
 * Redirects to login if user is not authenticated
 */

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { LoadingPage } from './LoadingSpinner';
import { UserRole } from '@/lib/types/user';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: UserRole;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requiredRole }) => {
  const { user, isLoading, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isLoading, isAuthenticated, router]);

  useEffect(() => {
    if (!isLoading && user && requiredRole && user.role !== requiredRole) {
      // User doesn't have required role, redirect to home
      router.push('/');
    }
  }, [isLoading, user, requiredRole, router]);

  if (isLoading) {
    return <LoadingPage />;
  }

  if (!isAuthenticated) {
    return null;
  }

  if (requiredRole && user?.role !== requiredRole) {
    return null;
  }

  return <>{children}</>;
};
