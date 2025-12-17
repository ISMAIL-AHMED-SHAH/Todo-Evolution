/**
 * useToast Hook
 *
 * Custom hook for managing toast notifications.
 * Provides a simple API for showing success, error, info, and warning toasts.
 * This is a lightweight implementation that will integrate with ShadCN Toast component.
 */

'use client';

import { useState, useCallback } from 'react';

/**
 * Toast Types
 */
export type ToastType = 'success' | 'error' | 'info' | 'warning';

/**
 * Toast Configuration
 */
export interface Toast {
  id: string;
  type: ToastType;
  title?: string;
  message: string;
  duration?: number; // milliseconds
  dismissible?: boolean;
}

/**
 * Toast State
 */
interface ToastState {
  toasts: Toast[];
}

/**
 * Toast Actions
 */
export interface ToastActions {
  toast: (config: Omit<Toast, 'id'>) => void;
  success: (message: string, title?: string) => void;
  error: (message: string, title?: string) => void;
  info: (message: string, title?: string) => void;
  warning: (message: string, title?: string) => void;
  dismiss: (id: string) => void;
  dismissAll: () => void;
}

/**
 * Default Toast Duration (in milliseconds)
 */
const DEFAULT_DURATION = 5000;

/**
 * Generate unique toast ID
 */
function generateToastId(): string {
  return `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * useToast Hook
 *
 * Manages toast notification state and provides actions for showing/dismissing toasts.
 *
 * @returns Toast state and action methods
 *
 * @example
 * ```tsx
 * function TaskForm() {
 *   const { success, error } = useToast();
 *
 *   const handleSubmit = async () => {
 *     try {
 *       await createTask(data);
 *       success('Task created successfully!');
 *     } catch (err) {
 *       error('Failed to create task. Please try again.');
 *     }
 *   };
 *
 *   return <form onSubmit={handleSubmit}>...</form>;
 * }
 * ```
 */
export function useToast(): ToastState & ToastActions {
  const [toasts, setToasts] = useState<Toast[]>([]);

  /**
   * Generic toast function
   */
  const toast = useCallback((config: Omit<Toast, 'id'>) => {
    const id = generateToastId();
    const duration = config.duration ?? DEFAULT_DURATION;

    const newToast: Toast = {
      ...config,
      id,
      duration,
      dismissible: config.dismissible ?? true,
    };

    setToasts((prev) => [...prev, newToast]);

    // Auto-dismiss after duration
    if (duration > 0) {
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, duration);
    }
  }, []);

  /**
   * Show success toast
   */
  const success = useCallback(
    (message: string, title?: string) => {
      toast({
        type: 'success',
        title: title || 'Success',
        message,
      });
    },
    [toast]
  );

  /**
   * Show error toast
   */
  const error = useCallback(
    (message: string, title?: string) => {
      toast({
        type: 'error',
        title: title || 'Error',
        message,
        duration: 7000, // Errors stay longer
      });
    },
    [toast]
  );

  /**
   * Show info toast
   */
  const info = useCallback(
    (message: string, title?: string) => {
      toast({
        type: 'info',
        title: title || 'Info',
        message,
      });
    },
    [toast]
  );

  /**
   * Show warning toast
   */
  const warning = useCallback(
    (message: string, title?: string) => {
      toast({
        type: 'warning',
        title: title || 'Warning',
        message,
        duration: 6000, // Warnings stay a bit longer
      });
    },
    [toast]
  );

  /**
   * Dismiss a specific toast by ID
   */
  const dismiss = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  /**
   * Dismiss all toasts
   */
  const dismissAll = useCallback(() => {
    setToasts([]);
  }, []);

  return {
    toasts,
    toast,
    success,
    error,
    info,
    warning,
    dismiss,
    dismissAll,
  };
}

/**
 * Toast Context Provider (Optional Enhancement)
 *
 * For global toast management across the app, you can wrap this hook in a context.
 * This is useful when you want to show toasts from anywhere in the component tree.
 */

// Note: This basic implementation will be enhanced when integrating with ShadCN Toast component.
// For now, components using this hook will manage their own toast state locally.
// To make it global, create a ToastContext and ToastProvider in a separate file.

/**
 * Example Global Toast Context Setup:
 *
 * // providers/toast-provider.tsx
 * 'use client';
 *
 * import { createContext, useContext, ReactNode } from 'react';
 * import { useToast, ToastActions, Toast } from '@/hooks/use-toast';
 *
 * const ToastContext = createContext<(ToastActions & { toasts: Toast[] }) | null>(null);
 *
 * export function ToastProvider({ children }: { children: ReactNode }) {
 *   const toast = useToast();
 *   return <ToastContext.Provider value={toast}>{children}</ToastContext.Provider>;
 * }
 *
 * export function useGlobalToast() {
 *   const context = useContext(ToastContext);
 *   if (!context) {
 *     throw new Error('useGlobalToast must be used within ToastProvider');
 *   }
 *   return context;
 * }
 */

export default useToast;
