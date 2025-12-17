/**
 * Validation utilities for form inputs
 */

export interface ValidationResult {
  isValid: boolean;
  error?: string;
}

/**
 * Validate email format
 */
export function validateEmail(email: string): ValidationResult {
  const trimmedEmail = email.trim();

  if (!trimmedEmail) {
    return { isValid: false, error: 'Email is required' };
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(trimmedEmail)) {
    return { isValid: false, error: 'Please enter a valid email address' };
  }

  return { isValid: true };
}

/**
 * Validate password strength
 */
export function validatePassword(password: string): ValidationResult {
  if (!password) {
    return { isValid: false, error: 'Password is required' };
  }

  if (password.length < 8) {
    return { isValid: false, error: 'Password must be at least 8 characters long' };
  }

  if (!/[A-Z]/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one uppercase letter' };
  }

  if (!/[a-z]/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one lowercase letter' };
  }

  if (!/[0-9]/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one number' };
  }

  return { isValid: true };
}

/**
 * Validate task title
 */
export function validateTaskTitle(title: string): ValidationResult {
  const trimmedTitle = title.trim();

  if (!trimmedTitle) {
    return { isValid: false, error: 'Title is required' };
  }

  if (trimmedTitle.length < 3) {
    return { isValid: false, error: 'Title must be at least 3 characters long' };
  }

  if (trimmedTitle.length > 200) {
    return { isValid: false, error: 'Title must be 200 characters or less' };
  }

  return { isValid: true };
}

/**
 * Validate task description
 */
export function validateTaskDescription(description?: string): ValidationResult {
  if (!description || description.trim() === '') {
    return { isValid: true }; // Description is optional
  }

  const trimmedDescription = description.trim();

  if (trimmedDescription.length > 1000) {
    return { isValid: false, error: 'Description must be 1000 characters or less' };
  }

  return { isValid: true };
}
