/**
 * User Type Definitions
 *
 * TypeScript types for user entities, authentication, and profile management.
 */

/**
 * User Entity (Database Model)
 *
 * Represents a user as stored in the database and returned by the API.
 */
export interface User {
  id: number;
  email: string;
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
}

/**
 * User Profile (Extended User Information)
 *
 * Extended user data including profile-specific fields.
 * Currently mirrors User but can be extended with additional fields
 * (e.g., name, avatar, preferences).
 */
export interface UserProfile extends User {
  // Future fields can be added here:
  // name?: string;
  // avatar_url?: string;
  // theme_preference?: 'light' | 'dark' | 'system';
  // timezone?: string;
}

/**
 * Authentication Session
 *
 * Represents an active user session with authentication token.
 */
export interface AuthSession {
  user: User;
  token: string; // JWT token
  expires_at: string; // ISO datetime
}

/**
 * Login Credentials
 *
 * Input data for login endpoint.
 */
export interface LoginCredentials {
  email: string;
  password: string;
}

/**
 * Registration Input
 *
 * Input data for user registration endpoint.
 */
export interface RegisterInput {
  email: string;
  password: string;
}

/**
 * Update Profile Input
 *
 * Fields allowed when updating user profile.
 */
export interface UpdateProfileInput {
  email?: string;
  // Future fields:
  // name?: string;
  // avatar_url?: string;
}

/**
 * Change Password Input
 *
 * Input data for password change endpoint.
 */
export interface ChangePasswordInput {
  current_password: string;
  new_password: string;
}

/**
 * Authentication State
 *
 * Client-side authentication state management.
 */
export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

/**
 * Better Auth Session Data
 *
 * Session data structure from Better Auth.
 */
export interface BetterAuthSession {
  user: User;
  session: {
    token: string;
    expiresAt: Date;
  };
}

/**
 * User Preferences (Future Extension)
 *
 * Placeholder for user preferences/settings.
 */
export interface UserPreferences {
  theme?: 'light' | 'dark' | 'system';
  language?: string;
  timezone?: string;
  notifications_enabled?: boolean;
  email_notifications?: boolean;
}

/**
 * Auth Error Types
 *
 * Standard authentication error codes.
 */
export type AuthErrorCode =
  | 'INVALID_CREDENTIALS'
  | 'EMAIL_ALREADY_EXISTS'
  | 'INVALID_TOKEN'
  | 'TOKEN_EXPIRED'
  | 'UNAUTHORIZED'
  | 'SESSION_EXPIRED'
  | 'UNKNOWN_ERROR';

/**
 * Authentication Error
 *
 * Structured error for authentication failures.
 */
export interface AuthError {
  code: AuthErrorCode;
  message: string;
  details?: Record<string, unknown>;
}

/**
 * Password Reset Request (Future)
 *
 * Input for password reset flow.
 */
export interface PasswordResetRequest {
  email: string;
}

/**
 * Password Reset Confirm (Future)
 *
 * Input for confirming password reset.
 */
export interface PasswordResetConfirm {
  token: string;
  new_password: string;
}

/**
 * Type Guards
 */

/**
 * Check if user is authenticated
 */
export function isAuthenticated(authState: AuthState): boolean {
  return authState.isAuthenticated && authState.user !== null;
}

/**
 * Check if email is valid format
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Check if password meets requirements
 * - Minimum 8 characters
 * - At least one uppercase letter
 * - At least one lowercase letter
 * - At least one number
 */
export function isValidPassword(password: string): boolean {
  if (password.length < 8) return false;

  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasNumber = /\d/.test(password);

  return hasUppercase && hasLowercase && hasNumber;
}

/**
 * Get password strength score (0-4)
 * 0 = Very weak
 * 1 = Weak
 * 2 = Fair
 * 3 = Good
 * 4 = Strong
 */
export function getPasswordStrength(password: string): number {
  let score = 0;

  // Length check
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;

  // Complexity checks
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
  if (/\d/.test(password)) score++;
  if (/[^a-zA-Z0-9]/.test(password)) score++; // Special characters

  return Math.min(score, 4);
}

/**
 * Get password strength label
 */
export function getPasswordStrengthLabel(password: string): string {
  const strength = getPasswordStrength(password);

  switch (strength) {
    case 0:
      return 'Very Weak';
    case 1:
      return 'Weak';
    case 2:
      return 'Fair';
    case 3:
      return 'Good';
    case 4:
      return 'Strong';
    default:
      return 'Unknown';
  }
}

/**
 * Sanitize user data for display
 * Removes sensitive fields before rendering in UI
 */
export function sanitizeUser(user: User): User {
  // Currently no sensitive fields to remove
  // Future: remove fields like password_hash, tokens, etc.
  return { ...user };
}

/**
 * Format user display name
 * Currently uses email, but can be extended to use actual name field
 */
export function getUserDisplayName(user: User): string {
  // Future: return user.name || user.email
  return user.email;
}

/**
 * Get user initials for avatar
 * Extracts initials from email (first letter before @)
 */
export function getUserInitials(user: User): string {
  const emailName = user.email.split('@')[0];
  return emailName.charAt(0).toUpperCase();
}
