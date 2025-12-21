/**
 * Navbar Component - Phase 2 UI/UX + Phase 9 Enhancements
 *
 * Top navigation bar with teal background
 * Features:
 * - T135: Mobile hamburger menu with responsive design
 * - T140: ARIA labels for accessibility
 * - T141: Keyboard navigation support (Tab, Enter, Escape)
 */

'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/use-auth';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Menu, X } from 'lucide-react';
import ThemeToggle from '@/components/ThemeToggle';

export default function Navbar() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  // T141: Close mobile menu on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isMobileMenuOpen) {
        setIsMobileMenuOpen(false);
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isMobileMenuOpen]);

  // Close mobile menu when clicking outside (on navigation)
  const closeMobileMenu = () => setIsMobileMenuOpen(false);

  return (
    <nav className="bg-teal-600 text-white shadow-md" role="navigation" aria-label="Main navigation">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo/Brand - T140: ARIA label */}
          <Link
            href="/dashboard"
            className="text-xl font-bold hover:text-teal-100 transition-colors"
            aria-label="ToDoneAI Home"
          >
            ToDoneAI
          </Link>

          {/* T135: Mobile Menu Toggle Button */}
          <button
            className="md:hidden p-2 rounded-md hover:bg-teal-700 transition-colors"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label={isMobileMenuOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={isMobileMenuOpen}
            aria-controls="mobile-menu"
          >
            {isMobileMenuOpen ? (
              <X className="h-6 w-6" aria-hidden="true" />
            ) : (
              <Menu className="h-6 w-6" aria-hidden="true" />
            )}
          </button>

          {/* Desktop Navigation Links - T140: ARIA labels */}
          <div className="hidden md:flex items-center gap-6" role="menubar">
            <Link
              href="/dashboard"
              className="hover:text-teal-100 transition-colors"
              role="menuitem"
              aria-label="Navigate to Dashboard"
            >
              Dashboard
            </Link>
            <Link
              href="/tasks"
              className="hover:text-teal-100 transition-colors"
              role="menuitem"
              aria-label="Navigate to Tasks"
            >
              Tasks
            </Link>
            <Link
              href="/profile"
              className="hover:text-teal-100 transition-colors"
              role="menuitem"
              aria-label="Navigate to Profile"
            >
              Profile
            </Link>
          </div>

          {/* Desktop User Section - T140: ARIA labels */}
          <div className="hidden md:flex items-center gap-3">
            <ThemeToggle />
            {user && (
              <span className="text-sm text-teal-100" aria-label={`Logged in as ${user.email}`}>
                {user.email}
              </span>
            )}
            <Button
              onClick={handleLogout}
              variant="secondary"
              size="sm"
              className="bg-white text-teal-600 hover:bg-teal-50"
              aria-label="Sign out of your account"
            >
              Sign Out
            </Button>
          </div>
        </div>

        {/* T135: Mobile Menu - Dropdown */}
        {isMobileMenuOpen && (
          <div
            id="mobile-menu"
            className="md:hidden py-4 border-t border-teal-500"
            role="menu"
            aria-label="Mobile navigation menu"
          >
            <div className="flex flex-col space-y-3">
              <Link
                href="/dashboard"
                className="px-4 py-2 hover:bg-teal-700 rounded transition-colors"
                onClick={closeMobileMenu}
                role="menuitem"
                aria-label="Navigate to Dashboard"
              >
                Dashboard
              </Link>
              <Link
                href="/tasks"
                className="px-4 py-2 hover:bg-teal-700 rounded transition-colors"
                onClick={closeMobileMenu}
                role="menuitem"
                aria-label="Navigate to Tasks"
              >
                Tasks
              </Link>
              <Link
                href="/profile"
                className="px-4 py-2 hover:bg-teal-700 rounded transition-colors"
                onClick={closeMobileMenu}
                role="menuitem"
                aria-label="Navigate to Profile"
              >
                Profile
              </Link>

              {/* Mobile User Section */}
              <div className="px-4 py-2 border-t border-teal-500 mt-2 pt-4">
                <div className="flex items-center justify-between mb-3">
                  {user && (
                    <p className="text-sm text-teal-100" aria-label={`Logged in as ${user.email}`}>
                      {user.email}
                    </p>
                  )}
                  <ThemeToggle />
                </div>
                <Button
                  onClick={() => {
                    closeMobileMenu();
                    handleLogout();
                  }}
                  variant="secondary"
                  size="sm"
                  className="w-full bg-white text-teal-600 hover:bg-teal-50"
                  aria-label="Sign out of your account"
                >
                  Sign Out
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
