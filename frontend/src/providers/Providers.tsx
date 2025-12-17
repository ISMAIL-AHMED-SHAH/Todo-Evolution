'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactNode, useState } from 'react'
import UserProviderWrapper from './UserProviderWrapper'
import Header from '@/components/Header'

interface ProvidersProps {
  children: ReactNode
}

/**
 * Root providers component that wraps the application with:
 * - React Query for data fetching and caching
 * - User authentication context
 * - Global layout components
 */
export function Providers({ children }: ProvidersProps) {
  // Create a new QueryClient instance for each request (Next.js 16 best practice)
  // This prevents state sharing between users on the server
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // Stale time: how long data is considered fresh
            staleTime: 5 * 60 * 1000, // 5 minutes
            // Cache time: how long unused data stays in cache
            gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
            // Retry failed requests
            retry: 1,
            // Refetch on window focus in production for fresh data
            refetchOnWindowFocus: process.env.NODE_ENV === 'production',
          },
          mutations: {
            // Retry failed mutations once
            retry: 1,
          },
        },
      })
  )

  return (
    <QueryClientProvider client={queryClient}>
      <UserProviderWrapper>
        <Header />
        {children}
      </UserProviderWrapper>
    </QueryClientProvider>
  )
}
