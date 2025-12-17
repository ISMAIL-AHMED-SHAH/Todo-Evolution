import React, { ReactNode } from 'react';

interface ResponsiveLayoutProps {
  children: ReactNode;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '4xl' | 'full';
  className?: string;
}

/**
 * ResponsiveLayout Component
 *
 * A reusable layout component that ensures consistent responsive behavior
 * across different screen sizes with mobile-first design principles.
 *
 * Features:
 * - Mobile-first responsive padding
 * - Configurable max-width for different content types
 * - Consistent spacing and alignment
 * - Touch-friendly spacing on mobile devices
 */
const ResponsiveLayout: React.FC<ResponsiveLayoutProps> = ({
  children,
  maxWidth = '4xl',
  className = ''
}) => {
  // Map maxWidth prop to Tailwind classes
  const maxWidthClasses = {
    'sm': 'max-w-sm',
    'md': 'max-w-md',
    'lg': 'max-w-lg',
    'xl': 'max-w-xl',
    '2xl': 'max-w-2xl',
    '4xl': 'max-w-4xl',
    'full': 'max-w-full'
  };

  return (
    <div className={`
      ${maxWidthClasses[maxWidth]}
      mx-auto
      px-4 sm:px-6 lg:px-8
      py-6 sm:py-8 lg:py-12
      w-full
      ${className}
    `.trim().replace(/\s+/g, ' ')}>
      {children}
    </div>
  );
};

export default ResponsiveLayout;
