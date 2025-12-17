/**
 * Login Page (T060)
 *
 * Renders the login form with link to register page
 */

import { Metadata } from 'next';
import Link from 'next/link';
import LoginForm from '@/components/auth/LoginForm';

export const metadata: Metadata = {
  title: 'Login - Todo App',
  description: 'Sign in to your Todo App account',
};

export default function LoginPage() {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 sm:p-8 w-full max-w-md mx-auto">
      <div className="mb-6">
        <h2 className="text-xl sm:text-2xl font-bold text-gray-900 text-center">
          Login
        </h2>
        <p className="text-sm text-gray-600 text-center mt-2">
          Welcome back! Please sign in to continue.
        </p>
      </div>

      <LoginForm />

      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600">
          Don&apos;t have an account?{' '}
          <Link
            href="/register"
            className="font-medium text-teal-600 hover:text-teal-500 transition-colors"
          >
            Create one here
          </Link>
        </p>
      </div>
    </div>
  );
}
