/**
 * Unit tests for validation utilities
 */

import {
  validateEmail,
  validatePassword,
  validateTaskTitle,
  validateTaskDescription,
} from '../utils/validation';

describe('Validation Utils', () => {
  describe('validateEmail', () => {
    it('should validate correct email addresses', () => {
      expect(validateEmail('test@example.com').isValid).toBe(true);
      expect(validateEmail('user.name@domain.co.uk').isValid).toBe(true);
    });

    it('should reject invalid email addresses', () => {
      expect(validateEmail('').isValid).toBe(false);
      expect(validateEmail('invalid').isValid).toBe(false);
      expect(validateEmail('no@domain').isValid).toBe(false);
      expect(validateEmail('@domain.com').isValid).toBe(false);
    });

    it('should provide error messages', () => {
      const result = validateEmail('');
      expect(result.isValid).toBe(false);
      expect(result.error).toBeDefined();
    });
  });

  describe('validatePassword', () => {
    it('should validate strong passwords', () => {
      expect(validatePassword('Password123').isValid).toBe(true);
      expect(validatePassword('Str0ngP@ss').isValid).toBe(true);
    });

    it('should reject weak passwords', () => {
      expect(validatePassword('').isValid).toBe(false);
      expect(validatePassword('short1A').isValid).toBe(false);
      expect(validatePassword('nouppercase1').isValid).toBe(false);
      expect(validatePassword('NOLOWERCASE1').isValid).toBe(false);
      expect(validatePassword('NoNumbers').isValid).toBe(false);
    });
  });

  describe('validateTaskTitle', () => {
    it('should validate correct task titles', () => {
      expect(validateTaskTitle('Buy groceries').isValid).toBe(true);
      expect(validateTaskTitle('A'.repeat(200)).isValid).toBe(true);
    });

    it('should reject invalid task titles', () => {
      expect(validateTaskTitle('').isValid).toBe(false);
      expect(validateTaskTitle('AB').isValid).toBe(false);
      expect(validateTaskTitle('A'.repeat(201)).isValid).toBe(false);
    });
  });

  describe('validateTaskDescription', () => {
    it('should validate correct task descriptions', () => {
      expect(validateTaskDescription('Some description').isValid).toBe(true);
      expect(validateTaskDescription('').isValid).toBe(true); // Optional
      expect(validateTaskDescription(undefined).isValid).toBe(true); // Optional
    });

    it('should reject overly long descriptions', () => {
      expect(validateTaskDescription('A'.repeat(1001)).isValid).toBe(false);
    });
  });
});
