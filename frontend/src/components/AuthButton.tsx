import React from 'react';
import Link from 'next/link';

interface AuthButtonProps {
  href: string;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
}

const AuthButton: React.FC<AuthButtonProps> = ({
  href,
  children,
  variant = 'primary'
}) => {
  const baseClasses = "inline-flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2";

  const variantClasses = variant === 'primary'
    ? "text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500"
    : "text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:ring-indigo-500";

  return (
    <Link href={href}>
      <button className={`${baseClasses} ${variantClasses}`}>
        {children}
      </button>
    </Link>
  );
};

export default AuthButton;