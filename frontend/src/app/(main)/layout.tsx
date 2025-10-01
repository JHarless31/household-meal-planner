'use client';

/**
 * Main application layout (for authenticated pages)
 */

import React from 'react';
import { Header } from '@/components/layout/Header';
import { Navigation } from '@/components/layout/Navigation';
import { Footer } from '@/components/layout/Footer';
import { ProtectedRoute } from '@/components/common/ProtectedRoute';

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ProtectedRoute>
      <div className="min-h-screen flex flex-col">
        <Header />
        <div className="flex-1 flex">
          <Navigation />
          <main className="flex-1 bg-gray-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
              {children}
            </div>
          </main>
        </div>
        <Footer />
      </div>
    </ProtectedRoute>
  );
}
