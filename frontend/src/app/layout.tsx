import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from '@/providers/Providers'
import { BetterAuthProvider } from '@/providers/BetterAuthProvider'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { Toaster } from '@/components/ui/toaster'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'ToDoneAI - Smart Task Management',
  description: 'Full-stack multi-user todo application with authentication and AI-powered features',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ErrorBoundary>
          <BetterAuthProvider>
            <Providers>
              {children}
              <Toaster />
            </Providers>
          </BetterAuthProvider>
        </ErrorBoundary>
      </body>
    </html>
  )
}
