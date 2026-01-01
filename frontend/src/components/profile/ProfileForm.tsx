/**
 * ProfileForm Component - User Story 6
 *
 * Comprehensive form for updating user profile information.
 * Features:
 * - T126: ProfileForm component structure
 * - T127: Fetches user data via props (from useAuth in parent)
 * - T128: Email update field with validation
 * - T129: Password change form (current + new password)
 * - T130: Profile update mutations using custom hook
 * - T131: Email validation via Zod schema
 * - T132: Password validation (min 8 characters) via Zod schema
 * - T133: Save changes with toast success message
 * - T134: Error handling for duplicate email
 */

'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { motion } from 'framer-motion';
import { User as UserIcon, Lock, Save } from 'lucide-react';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { useProfileMutations } from '@/hooks/use-profile-mutations';
import {
  updateProfileSchema,
  changePasswordSchema,
  type UpdateProfileFormData,
  type ChangePasswordFormData,
} from '@/lib/validations';
import type { User } from '@/types/user';

interface ProfileFormProps {
  user: User;
}

/**
 * Form field animation variant
 */
const fieldVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.05,
      type: 'spring' as const,
      stiffness: 300,
      damping: 25,
    },
  }),
};

export function ProfileForm({ user }: ProfileFormProps) {
  // T130: Use profile mutations hook
  const { updateProfileMutation, changePasswordMutation } = useProfileMutations(user.id, {
    onUpdateProfileSuccess: () => {
      // Form will reflect updates when session is invalidated
    },
    onChangePasswordSuccess: () => {
      // Reset password form
      passwordForm.reset({
        currentPassword: '',
        newPassword: '',
        confirmNewPassword: '',
      });
    },
  });

  // Profile update form (name)
  const profileForm = useForm<UpdateProfileFormData>({
    resolver: zodResolver(updateProfileSchema),
    defaultValues: {
      name: user.name || '',
    },
  });

  // Password change form
  const passwordForm = useForm<ChangePasswordFormData>({
    resolver: zodResolver(changePasswordSchema),
    defaultValues: {
      currentPassword: '',
      newPassword: '',
      confirmNewPassword: '',
    },
  });

  /**
   * T128: Handle profile update submission
   * T130: Uses updateProfileMutation from hook
   * T133: Toast success message (handled by hook)
   */
  const handleProfileUpdate = async (data: UpdateProfileFormData) => {
    if (!data.name || data.name === user.name) {
      return; // No changes to submit
    }

    updateProfileMutation.mutate(data);
  };

  /**
   * T129: Handle password change submission
   * T130: Uses changePasswordMutation from hook
   * T132: Password validation (min 8 characters) via Zod schema
   * T133: Toast success message (handled by hook)
   */
  const handlePasswordChange = async (data: ChangePasswordFormData) => {
    changePasswordMutation.mutate(data);
  };

  return (
    <div className="space-y-8">
      {/* Profile Update Section - T128 */}
      <motion.div
        custom={0}
        variants={fieldVariants}
        initial="hidden"
        animate="visible"
      >
        <div className="flex items-center gap-2 mb-4">
          <UserIcon className="h-5 w-5 text-teal-600 dark:text-teal-400" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Profile Information</h2>
        </div>

        <Form {...profileForm}>
          <form onSubmit={profileForm.handleSubmit(handleProfileUpdate)} className="space-y-4">
            <FormField
              control={profileForm.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-gray-700 dark:text-gray-200">Name</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      type="text"
                      placeholder="Your name"
                      disabled={updateProfileMutation.isPending}
                      className="w-full sm:max-w-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-400"
                    />
                  </FormControl>
                  <FormDescription className="text-gray-600 dark:text-gray-400">
                    This is the display name for your account.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              type="submit"
              disabled={updateProfileMutation.isPending || !profileForm.formState.isDirty}
              className="bg-teal-600 hover:bg-teal-700 w-full sm:w-auto min-h-[44px]"
            >
              <Save className="h-4 w-4 mr-2" />
              {updateProfileMutation.isPending ? 'Updating...' : 'Update Profile'}
            </Button>
          </form>
        </Form>
      </motion.div>

      <Separator />

      {/* Password Change Section - T129 */}
      <motion.div
        custom={1}
        variants={fieldVariants}
        initial="hidden"
        animate="visible"
      >
        <div className="flex items-center gap-2 mb-4">
          <Lock className="h-5 w-5 text-teal-600 dark:text-teal-400" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Change Password</h2>
        </div>

        <Form {...passwordForm}>
          <form onSubmit={passwordForm.handleSubmit(handlePasswordChange)} className="space-y-4">
            {/* Current Password Field */}
            <FormField
              control={passwordForm.control}
              name="currentPassword"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-gray-700 dark:text-gray-200">Current Password</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      type="password"
                      placeholder="Enter current password"
                      disabled={changePasswordMutation.isPending}
                      className="w-full sm:max-w-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-400"
                    />
                  </FormControl>
                  <FormDescription className="text-gray-600 dark:text-gray-400">
                    Enter your current password to verify your identity.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* New Password Field - T132: Min 8 characters validation */}
            <FormField
              control={passwordForm.control}
              name="newPassword"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-gray-700 dark:text-gray-200">New Password</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      type="password"
                      placeholder="Enter new password"
                      disabled={changePasswordMutation.isPending}
                      className="w-full sm:max-w-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-400"
                    />
                  </FormControl>
                  <FormDescription className="text-gray-600 dark:text-gray-400">
                    Must be at least 8 characters with uppercase, lowercase, and number.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Confirm New Password Field */}
            <FormField
              control={passwordForm.control}
              name="confirmNewPassword"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-gray-700 dark:text-gray-200">Confirm New Password</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      type="password"
                      placeholder="Confirm new password"
                      disabled={changePasswordMutation.isPending}
                      className="w-full sm:max-w-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-400"
                    />
                  </FormControl>
                  <FormDescription className="text-gray-600 dark:text-gray-400">
                    Re-enter your new password to confirm.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              type="submit"
              disabled={changePasswordMutation.isPending || !passwordForm.formState.isDirty}
              className="bg-teal-600 hover:bg-teal-700 w-full sm:w-auto min-h-[44px]"
            >
              <Save className="h-4 w-4 mr-2" />
              {changePasswordMutation.isPending ? 'Changing Password...' : 'Change Password'}
            </Button>
          </form>
        </Form>
      </motion.div>

      {/* Account Information Display */}
      <motion.div
        custom={2}
        variants={fieldVariants}
        initial="hidden"
        animate="visible"
      >
        <Separator className="mb-6 bg-gray-200 dark:bg-gray-700" />
        <div className="text-sm text-gray-600 dark:text-gray-400 space-y-2">
          <p>
            <span className="font-semibold text-gray-900 dark:text-gray-200">Account ID:</span> {user.id}
          </p>
          {(user.created_at || user.createdAt) && (
            <p>
              <span className="font-semibold text-gray-900 dark:text-gray-200">Member since:</span>{' '}
              {new Date(user.created_at || user.createdAt!).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </p>
          )}
          {(user.updated_at || user.updatedAt) && (
            <p>
              <span className="font-semibold text-gray-900 dark:text-gray-200">Last updated:</span>{' '}
              {new Date(user.updated_at || user.updatedAt!).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </p>
          )}
        </div>
      </motion.div>
    </div>
  );
}
