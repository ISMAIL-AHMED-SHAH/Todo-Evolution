/**
 * Better Auth Provider (T065 - Part of Better Auth Session Integration)
 *
 * Wraps the application with Better Auth context
 * - Ensures Better Auth client is initialized
 * - Provides session management across the app
 * - Works with the useAuth hook from hooks/use-auth.ts
 */

'use client';

import { ReactNode } from 'react';

interface BetterAuthProviderProps {
  children: ReactNode;
}

/**
 * BetterAuthProvider Component
 *
 * Better Auth handles session management internally through the authClient.
 * This provider ensures the client-side context is properly set up.
 * The actual session state is managed by the useAuth hook.
 */
export function BetterAuthProvider({ children }: BetterAuthProviderProps) {
  // Better Auth doesn't require a specific provider wrapper
  // Session management is handled by the authClient and useAuth hook
  // This component exists for clarity and future extensibility
  return <>{children}</>;
}
