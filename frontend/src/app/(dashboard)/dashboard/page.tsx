/**
 * Dashboard Page (Demo for Testing Auth Components)
 *
 * Protected page that requires authentication
 * Uses the new ProtectedRoute component
 */

'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { useAuth } from '@/hooks/use-auth';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Dashboard
            </h1>
            <p className="text-lg text-gray-600 mb-6">
              Welcome back, {user?.email}!
            </p>
            <div className="flex gap-4">
              <Button
                onClick={handleLogout}
                variant="outline"
              >
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
