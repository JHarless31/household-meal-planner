import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { AuthProvider } from '@/contexts/AuthContext';
import { ToastProvider } from '@/contexts/ToastContext';
import { ToastContainer } from '@/components/common/Toast';
import '@/styles/globals.css';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata: Metadata = {
  title: 'Meal Planning App',
  description: 'Plan your meals, manage inventory, and organize your kitchen',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="font-sans antialiased">
        <ToastProvider>
          <AuthProvider>
            {children}
            <ToastContainer />
          </AuthProvider>
        </ToastProvider>
      </body>
    </html>
  );
}
