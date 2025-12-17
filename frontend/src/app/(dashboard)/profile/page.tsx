"use client";

import { motion } from "framer-motion";
import { User } from "lucide-react";
import { useAuth } from "@/hooks/use-auth";
import { ProfileForm } from "@/components/profile/ProfileForm";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";

// Page transition animation variants
const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

/**
 * Profile Page - User Story 6
 *
 * Allows users to view and update their profile information.
 * Features:
 * - T125: Profile page with user information display
 * - T127: Fetches user data from auth context
 * - Framer Motion page transitions
 * - Loading and error states
 */
export default function ProfilePage() {
  const { user, isLoading, error } = useAuth();

  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ duration: 0.3 }}
      className="container mx-auto px-3 sm:px-4 py-4 sm:py-8 max-w-3xl"
    >
      {/* Page Header */}
      <div className="flex items-center gap-2 sm:gap-3 mb-6 sm:mb-8">
        <div className="p-2 sm:p-3 bg-teal-100 rounded-full">
          <User className="h-5 w-5 sm:h-6 sm:w-6 text-teal-600" />
        </div>
        <div className="min-w-0 flex-1">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 break-words">Profile Settings</h1>
          <p className="text-sm sm:text-base text-gray-600 mt-1">
            Manage your account information and preferences
          </p>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="space-y-6">
          <Skeleton className="h-24 w-full" />
          <Skeleton className="h-64 w-full" />
        </div>
      )}

      {/* Error State */}
      {error && !isLoading && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>
            {error || "Failed to load profile. Please try again later."}
          </AlertDescription>
        </Alert>
      )}

      {/* Success State */}
      {!isLoading && !error && user && (
        <div className="bg-white rounded-lg shadow-sm border p-4 sm:p-6">
          <ProfileForm user={user} />
        </div>
      )}

      {/* Not Authenticated State */}
      {!isLoading && !error && !user && (
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Not Authenticated</AlertTitle>
          <AlertDescription>
            Please log in to view your profile.
          </AlertDescription>
        </Alert>
      )}
    </motion.div>
  );
}
