/**
 * CategoryInput Component
 *
 * Multi-tag input component for task categories.
 * Allows adding, removing, and validating category tags.
 */

'use client';

import { useState, KeyboardEvent } from 'react';
import { X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { categorySchema } from '@/lib/validations';

interface CategoryInputProps {
  value: string[];
  onChange: (categories: string[]) => void;
  maxCategories?: number;
  placeholder?: string;
  disabled?: boolean;
}

/**
 * Tag animation variants
 */
const tagVariants = {
  hidden: { opacity: 0, scale: 0.8, y: -10 },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: { type: 'spring' as const, stiffness: 300, damping: 25 },
  },
  exit: {
    opacity: 0,
    scale: 0.8,
    x: -10,
    transition: { duration: 0.15 },
  },
};

export function CategoryInput({
  value = [],
  onChange,
  maxCategories = 10,
  placeholder = 'Add category and press Enter...',
  disabled = false,
}: CategoryInputProps) {
  const [inputValue, setInputValue] = useState('');
  const [error, setError] = useState<string | null>(null);

  /**
   * Add a new category tag
   */
  const addCategory = () => {
    const trimmed = inputValue.trim();

    // Clear error
    setError(null);

    // Validate input
    if (!trimmed) {
      return;
    }

    // Check max categories
    if (value.length >= maxCategories) {
      setError(`Maximum ${maxCategories} categories allowed`);
      return;
    }

    // Check for duplicates (case-insensitive)
    if (value.some((cat) => cat.toLowerCase() === trimmed.toLowerCase())) {
      setError('Category already exists');
      return;
    }

    // Validate with Zod schema
    const result = categorySchema.safeParse(trimmed);
    if (!result.success) {
      setError(result.error.issues[0]?.message || 'Invalid category');
      return;
    }

    // Add category
    onChange([...value, trimmed]);
    setInputValue('');
  };

  /**
   * Remove a category tag
   */
  const removeCategory = (index: number) => {
    const newCategories = value.filter((_, i) => i !== index);
    onChange(newCategories);
    setError(null);
  };

  /**
   * Handle keyboard events
   */
  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addCategory();
    } else if (e.key === 'Backspace' && !inputValue && value.length > 0) {
      // Remove last category on backspace if input is empty
      removeCategory(value.length - 1);
    }
  };

  /**
   * Handle input change
   */
  const handleInputChange = (newValue: string) => {
    setInputValue(newValue);
    setError(null);
  };

  return (
    <div className="space-y-2">
      {/* Category tags display */}
      {value.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-2">
          <AnimatePresence mode="popLayout">
            {value.map((category, index) => (
              <motion.div
                key={`${category}-${index}`}
                variants={tagVariants}
                initial="hidden"
                animate="visible"
                exit="exit"
                layout
              >
                <Badge
                  variant="secondary"
                  className="pl-3 pr-2 py-1.5 flex items-center gap-1.5 bg-blue-100 dark:bg-blue-900/30 text-blue-900 dark:text-blue-200 hover:bg-blue-200 dark:hover:bg-blue-900/40 transition-colors border border-blue-200 dark:border-blue-800"
                >
                  <span className="text-sm font-medium">{category}</span>
                  <button
                    type="button"
                    onClick={() => removeCategory(index)}
                    disabled={disabled}
                    className="ml-1 rounded-full hover:bg-blue-300 dark:hover:bg-blue-800 transition-colors p-0.5 focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                    aria-label={`Remove ${category}`}
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}

      {/* Input field */}
      <div>
        <Input
          type="text"
          value={inputValue}
          onChange={(e) => handleInputChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled || value.length >= maxCategories}
          className={`h-11 bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-400 ${error ? 'border-red-500 focus:ring-red-500' : ''}`}
          aria-invalid={!!error}
          aria-describedby={error ? 'category-error' : undefined}
        />

        {/* Helper text */}
        <div className="flex justify-between items-center mt-1.5 text-xs">
          {error ? (
            <p id="category-error" className="text-red-600 dark:text-red-400">
              {error}
            </p>
          ) : (
            <p className="text-gray-500 dark:text-gray-400">
              Press Enter to add
            </p>
          )}
          <p className="text-gray-400 dark:text-gray-500">
            {value.length}/{maxCategories}
          </p>
        </div>
      </div>
    </div>
  );
}
