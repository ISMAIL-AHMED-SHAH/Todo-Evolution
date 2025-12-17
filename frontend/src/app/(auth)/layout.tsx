/**
 * Auth Layout (T059)
 *
 * Centered layout for authentication pages (login, register)
 * - No navbar for clean auth experience
 * - Centered content with app branding
 */

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-teal-50 to-blue-50 px-4 sm:px-6 py-8 sm:py-12">
      {/* App Branding */}
      <div className="mb-6 sm:mb-8 text-center">
        <h1 className="text-3xl sm:text-4xl font-bold text-teal-600 mb-2">
          Todo App
        </h1>
        <p className="text-sm sm:text-base text-gray-600">
          Organize your day, achieve your goals
        </p>
      </div>

      {/* Auth Content */}
      <div className="w-full max-w-md">
        {children}
      </div>

      {/* Footer */}
      <div className="mt-6 sm:mt-8 text-center text-xs sm:text-sm text-gray-500">
        <p>&copy; 2025 Todo App. All rights reserved.</p>
      </div>
    </div>
  );
}
