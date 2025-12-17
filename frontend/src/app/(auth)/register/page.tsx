/**
 * Register Page (T061)
 *
 * Renders the registration form with link to login page
 */

import { Metadata } from 'next';
import Link from 'next/link';
import RegisterForm from '@/components/auth/RegisterForm';

export const metadata: Metadata = {
  title: 'Register - Todo App',
  description: 'Create your Todo App account',
};

export default function RegisterPage() {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 sm:p-8 w-full max-w-md mx-auto">
      <div className="mb-6">
        <h2 className="text-xl sm:text-2xl font-bold text-gray-900 text-center">
          Register
        </h2>
        <p className="text-sm text-gray-600 text-center mt-2">
          Create your account to start managing your tasks.
        </p>
      </div>

      <RegisterForm />

      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600">
          Already have an account?{' '}
          <Link
            href="/login"
            className="font-medium text-teal-600 hover:text-teal-500 transition-colors"
          >
            Sign in here
          </Link>
        </p>
      </div>
    </div>
  );
}
