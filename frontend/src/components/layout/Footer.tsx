/**
 * Application Footer component
 */

import React from 'react';
import { APP_NAME, APP_VERSION } from '@/lib/utils/constants';

export const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center text-sm text-gray-500">
          <p>
            © {currentYear} {APP_NAME}. All rights reserved.
          </p>
          <p>Version {APP_VERSION}</p>
        </div>
      </div>
    </footer>
  );
};
