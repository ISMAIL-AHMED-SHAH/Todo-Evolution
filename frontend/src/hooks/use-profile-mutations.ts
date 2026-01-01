/**
 * useProfileMutations - React Query mutations for profile operations
 *
 * Provides update email and change password mutations
 */

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { authClient } from "@/lib/auth-client";
import type { User } from "@/types/user";

interface UpdateProfileData {
  name?: string;
  image?: string | null;
}

interface ChangePasswordData {
  currentPassword: string;
  newPassword: string;
}

interface UseProfileMutationsOptions {
  onUpdateProfileSuccess?: () => void;
  onChangePasswordSuccess?: () => void;
  onError?: (error: Error) => void;
}

/**
 * Hook for profile mutations (update email, change password)
 */
export function useProfileMutations(
  userId: string,
  options: UseProfileMutationsOptions = {}
) {
  const queryClient = useQueryClient();

  // Update profile mutation (name, image)
  const updateProfileMutation = useMutation({
    mutationFn: async (data: UpdateProfileData): Promise<void> => {
      // Use Better Auth to update user profile
      const response = await authClient.updateUser(data);
      if (!response.data?.status) {
        throw new Error("Failed to update profile");
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user", userId] });
      // Refetch session to get updated user data
      queryClient.invalidateQueries({ queryKey: ["session"] });
      options.onUpdateProfileSuccess?.();
    },
    onError: options.onError,
  });

  // Change password mutation
  const changePasswordMutation = useMutation({
    mutationFn: async (data: ChangePasswordData): Promise<void> => {
      // Use Better Auth to change password
      const response = await authClient.changePassword({
        newPassword: data.newPassword,
        currentPassword: data.currentPassword,
        revokeOtherSessions: false,
      });

      if (!response.data) {
        throw new Error("Failed to change password");
      }
    },
    onSuccess: () => {
      options.onChangePasswordSuccess?.();
    },
    onError: options.onError,
  });

  return {
    updateProfileMutation,
    changePasswordMutation,
  };
}
