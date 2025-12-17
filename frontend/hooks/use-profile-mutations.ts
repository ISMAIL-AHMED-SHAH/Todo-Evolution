/**
 * useProfileMutations Hook - T130
 *
 * Custom React Query hook for profile mutations (update email, change password).
 * Provides error handling, toast notifications, and callback support.
 */

'use client';

import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { useToast } from '../src/hooks/use-toast';
import type { User } from '@/types/user';
import type { ApiErrorResponse } from '@/types/api';
import type { UpdateProfileFormData, ChangePasswordFormData } from '@/lib/validations';

/**
 * Update Profile Email Input
 */
interface UpdateEmailInput {
  email: string;
}

/**
 * Change Password Input
 */
interface ChangePasswordInput {
  current_password: string;
  new_password: string;
}

/**
 * Update Profile Email Mutation
 */
async function updateProfileEmail(userId: number, input: UpdateEmailInput): Promise<User> {
  const endpoint = `/api/${userId}/profile`;
  const response = await apiClient.put<User | { user: User }>(endpoint, input);

  // Handle different response formats
  if (response && typeof response === 'object' && 'user' in response) {
    return response.user;
  }

  return response as User;
}

/**
 * Change Password Mutation
 */
async function changePassword(userId: number, input: ChangePasswordInput): Promise<void> {
  const endpoint = `/api/${userId}/password`;
  await apiClient.put<void>(endpoint, input);
}

/**
 * useProfileMutations Hook
 *
 * Provides mutation functions for profile operations with error handling.
 *
 * @param userId - The ID of the user performing mutations
 * @param options - Optional callbacks for success/error handling
 *
 * @example
 * ```tsx
 * function ProfileForm() {
 *   const userId = useUserId();
 *   const { updateEmailMutation, changePasswordMutation } = useProfileMutations(userId, {
 *     onUpdateEmailSuccess: () => console.log('Email updated'),
 *     onChangePasswordSuccess: () => console.log('Password changed'),
 *   });
 *
 *   const handleEmailUpdate = () => {
 *     updateEmailMutation.mutate({ email: 'new@example.com' });
 *   };
 *
 *   return <button onClick={handleEmailUpdate}>Update Email</button>;
 * }
 * ```
 */
export function useProfileMutations(
  userId: number | null,
  options?: {
    onUpdateEmailSuccess?: (user: User) => void;
    onChangePasswordSuccess?: () => void;
    onError?: (error: ApiErrorResponse) => void;
  }
) {
  const { toast } = useToast();

  /**
   * Update Email Mutation
   */
  const updateEmailMutation: UseMutationResult<User, ApiErrorResponse, UpdateProfileFormData> =
    useMutation<User, ApiErrorResponse, UpdateProfileFormData>({
      mutationFn: (input: UpdateProfileFormData) => {
        if (!userId) {
          throw new Error('User ID is required');
        }
        if (!input.email) {
          throw new Error('Email is required');
        }
        return updateProfileEmail(userId, { email: input.email });
      },

      onSuccess: (user) => {
        // Show success toast
        toast({
          title: 'Email Updated',
          description: 'Your email address has been updated successfully.',
          variant: 'default',
        });

        options?.onUpdateEmailSuccess?.(user);
      },

      onError: (error) => {
        // Determine error message
        const errorMessage = error?.error?.message || 'Failed to update email';

        // Check for duplicate email error
        const isDuplicateEmail =
          errorMessage.toLowerCase().includes('already exists') ||
          errorMessage.toLowerCase().includes('duplicate');

        // Show error toast
        toast({
          title: 'Update Failed',
          description: isDuplicateEmail
            ? 'This email address is already in use. Please use a different email.'
            : errorMessage,
          variant: 'destructive',
        });

        options?.onError?.(error);
      },
    });

  /**
   * Change Password Mutation
   */
  const changePasswordMutation: UseMutationResult<void, ApiErrorResponse, ChangePasswordFormData> =
    useMutation<void, ApiErrorResponse, ChangePasswordFormData>({
      mutationFn: (input: ChangePasswordFormData) => {
        if (!userId) {
          throw new Error('User ID is required');
        }
        return changePassword(userId, {
          current_password: input.currentPassword,
          new_password: input.newPassword,
        });
      },

      onSuccess: () => {
        // Show success toast
        toast({
          title: 'Password Changed',
          description: 'Your password has been changed successfully.',
          variant: 'default',
        });

        options?.onChangePasswordSuccess?.();
      },

      onError: (error) => {
        // Determine error message
        const errorMessage = error?.error?.message || 'Failed to change password';

        // Check for incorrect current password error
        const isIncorrectPassword =
          errorMessage.toLowerCase().includes('incorrect') ||
          errorMessage.toLowerCase().includes('wrong');

        // Show error toast
        toast({
          title: 'Password Change Failed',
          description: isIncorrectPassword
            ? 'Current password is incorrect. Please try again.'
            : errorMessage,
          variant: 'destructive',
        });

        options?.onError?.(error);
      },
    });

  return {
    updateEmailMutation,
    changePasswordMutation,
  };
}

/**
 * Convenience hook for updating email only
 */
export function useUpdateEmail(
  userId: number | null,
  options?: { onSuccess?: (user: User) => void; onError?: (error: ApiErrorResponse) => void }
) {
  const { updateEmailMutation } = useProfileMutations(userId, {
    onUpdateEmailSuccess: options?.onSuccess,
    onError: options?.onError,
  });
  return updateEmailMutation;
}

/**
 * Convenience hook for changing password only
 */
export function useChangePassword(
  userId: number | null,
  options?: { onSuccess?: () => void; onError?: (error: ApiErrorResponse) => void }
) {
  const { changePasswordMutation } = useProfileMutations(userId, {
    onChangePasswordSuccess: options?.onSuccess,
    onError: options?.onError,
  });
  return changePasswordMutation;
}
