/**
 * API Type Definitions
 *
 * TypeScript types for API requests, responses, and error handling.
 */

import { Task, TaskStats } from './task';
import { User } from './user';

/**
 * HTTP Methods
 */
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

/**
 * API Response Status Codes
 */
export type ApiStatusCode =
  | 200 // OK
  | 201 // Created
  | 204 // No Content
  | 400 // Bad Request
  | 401 // Unauthorized
  | 403 // Forbidden
  | 404 // Not Found
  | 409 // Conflict
  | 422 // Unprocessable Entity
  | 500; // Internal Server Error

/**
 * Generic API Response Wrapper
 */
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  timestamp?: string;
}

/**
 * Generic API Error Response
 */
export interface ApiErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
    status_code?: number;
  };
  timestamp?: string;
}

/**
 * Validation Error Detail
 *
 * Used for 422 Unprocessable Entity responses
 */
export interface ValidationErrorDetail {
  field: string;
  message: string;
  type?: string;
}

/**
 * Validation Error Response
 */
export interface ValidationErrorResponse extends ApiErrorResponse {
  error: {
    code: 'VALIDATION_ERROR';
    message: string;
    details: {
      errors: ValidationErrorDetail[];
    };
    status_code: 422;
  };
}

/**
 * Paginated Response
 *
 * Generic pagination wrapper for list endpoints
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

/**
 * Pagination Parameters
 */
export interface PaginationParams {
  page?: number;
  page_size?: number;
  limit?: number;
  offset?: number;
}

/**
 * Task API Responses
 */

// List tasks response
export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

// Single task response
export interface TaskResponse {
  task: Task;
}

// Task statistics response
export interface TaskStatsResponse {
  stats: TaskStats;
}

// Task creation success response
export interface TaskCreateResponse {
  task: Task;
  message: string;
}

// Task update success response
export interface TaskUpdateResponse {
  task: Task;
  message: string;
}

// Task deletion success response
export interface TaskDeleteResponse {
  success: boolean;
  message: string;
}

/**
 * User/Auth API Responses
 */

// Login success response
export interface LoginResponse {
  user: User;
  token: string;
  expires_at: string; // ISO datetime
}

// Registration success response
export interface RegisterResponse {
  user: User;
  token: string;
  message: string;
}

// Profile response
export interface ProfileResponse {
  user: User;
}

// Profile update success response
export interface ProfileUpdateResponse {
  user: User;
  message: string;
}

// Logout success response
export interface LogoutResponse {
  success: boolean;
  message: string;
}

/**
 * API Error Codes
 */
export enum ApiErrorCode {
  // Authentication errors (401)
  INVALID_CREDENTIALS = 'INVALID_CREDENTIALS',
  INVALID_TOKEN = 'INVALID_TOKEN',
  TOKEN_EXPIRED = 'TOKEN_EXPIRED',
  UNAUTHORIZED = 'UNAUTHORIZED',

  // Authorization errors (403)
  FORBIDDEN = 'FORBIDDEN',
  INSUFFICIENT_PERMISSIONS = 'INSUFFICIENT_PERMISSIONS',

  // Resource errors (404)
  NOT_FOUND = 'NOT_FOUND',
  TASK_NOT_FOUND = 'TASK_NOT_FOUND',
  USER_NOT_FOUND = 'USER_NOT_FOUND',

  // Validation errors (400, 422)
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  INVALID_INPUT = 'INVALID_INPUT',
  MISSING_REQUIRED_FIELD = 'MISSING_REQUIRED_FIELD',

  // Conflict errors (409)
  CONFLICT = 'CONFLICT',
  EMAIL_ALREADY_EXISTS = 'EMAIL_ALREADY_EXISTS',
  DUPLICATE_RESOURCE = 'DUPLICATE_RESOURCE',

  // Server errors (500)
  INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR',
  DATABASE_ERROR = 'DATABASE_ERROR',
  UNKNOWN_ERROR = 'UNKNOWN_ERROR',

  // Network errors (client-side)
  NETWORK_ERROR = 'NETWORK_ERROR',
  REQUEST_TIMEOUT = 'REQUEST_TIMEOUT',
}

/**
 * API Request Configuration
 */
export interface ApiRequestConfig {
  method: HttpMethod;
  url: string;
  headers?: Record<string, string>;
  body?: unknown;
  params?: Record<string, string | number | boolean>;
  timeout?: number; // milliseconds
  signal?: AbortSignal; // For request cancellation
}

/**
 * API Client Configuration
 */
export interface ApiClientConfig {
  baseUrl: string;
  timeout?: number;
  headers?: Record<string, string>;
  withCredentials?: boolean;
  onRequest?: (config: ApiRequestConfig) => ApiRequestConfig | Promise<ApiRequestConfig>;
  onResponse?: <T>(response: ApiResponse<T>) => ApiResponse<T> | Promise<ApiResponse<T>>;
  onError?: (error: ApiErrorResponse) => void | Promise<void>;
}

/**
 * Fetch Options
 */
export interface FetchOptions extends Omit<RequestInit, 'body' | 'method'> {
  params?: Record<string, string | number | boolean>;
  timeout?: number;
}

/**
 * Type Guards
 */

/**
 * Check if response is an error response
 */
export function isApiError(response: unknown): response is ApiErrorResponse {
  return (
    typeof response === 'object' &&
    response !== null &&
    'success' in response &&
    response.success === false &&
    'error' in response
  );
}

/**
 * Check if error is a validation error
 */
export function isValidationError(error: ApiErrorResponse): error is ValidationErrorResponse {
  return error.error.code === 'VALIDATION_ERROR';
}

/**
 * Check if error is authentication error
 */
export function isAuthError(error: ApiErrorResponse): boolean {
  const authErrorCodes: string[] = [
    ApiErrorCode.INVALID_CREDENTIALS,
    ApiErrorCode.INVALID_TOKEN,
    ApiErrorCode.TOKEN_EXPIRED,
    ApiErrorCode.UNAUTHORIZED,
  ];
  return authErrorCodes.includes(error.error.code);
}

/**
 * Check if error is a network error
 */
export function isNetworkError(error: unknown): boolean {
  return (
    error instanceof TypeError ||
    (error instanceof Error && error.message.includes('network')) ||
    (isApiError(error) && error.error.code === ApiErrorCode.NETWORK_ERROR)
  );
}

/**
 * Utility Functions
 */

/**
 * Build URL with query parameters
 */
export function buildUrl(baseUrl: string, params?: Record<string, string | number | boolean>): string {
  if (!params || Object.keys(params).length === 0) {
    return baseUrl;
  }

  const url = new URL(baseUrl, window.location.origin);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      url.searchParams.append(key, String(value));
    }
  });

  return url.toString();
}

/**
 * Extract error message from API error response
 */
export function getErrorMessage(error: unknown, defaultMessage = 'An error occurred'): string {
  if (isApiError(error)) {
    return error.error.message || defaultMessage;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return defaultMessage;
}

/**
 * Extract validation errors from validation error response
 */
export function getValidationErrors(error: ApiErrorResponse): ValidationErrorDetail[] {
  if (isValidationError(error)) {
    return error.error.details.errors;
  }
  return [];
}

/**
 * Create an API error response
 */
export function createApiError(
  code: ApiErrorCode | string,
  message: string,
  statusCode?: number,
  details?: Record<string, unknown>
): ApiErrorResponse {
  return {
    success: false,
    error: {
      code,
      message,
      status_code: statusCode,
      details,
    },
    timestamp: new Date().toISOString(),
  };
}

/**
 * HTTP Status Code Helpers
 */

export function isSuccessStatus(status: number): boolean {
  return status >= 200 && status < 300;
}

export function isClientErrorStatus(status: number): boolean {
  return status >= 400 && status < 500;
}

export function isServerErrorStatus(status: number): boolean {
  return status >= 500 && status < 600;
}

/**
 * API Endpoint Paths
 *
 * Centralized endpoint path definitions
 */
export const API_ENDPOINTS = {
  // Auth endpoints
  auth: {
    login: '/auth/login',
    register: '/auth/register',
    logout: '/auth/logout',
    refresh: '/auth/refresh',
    session: '/auth/session',
  },

  // User endpoints
  users: {
    profile: (userId: string) => `/api/${userId}/profile`,
    updateProfile: (userId: string) => `/api/${userId}/profile`,
  },

  // Task endpoints
  tasks: {
    list: (userId: string) => `/api/${userId}/tasks`,
    create: (userId: string) => `/api/${userId}/tasks`,
    get: (userId: string, taskId: number) => `/api/${userId}/tasks/${taskId}`,
    update: (userId: string, taskId: number) => `/api/${userId}/tasks/${taskId}`,
    delete: (userId: string, taskId: number) => `/api/${userId}/tasks/${taskId}`,
    complete: (userId: string, taskId: number) => `/api/${userId}/tasks/${taskId}/complete`,
    stats: (userId: string) => `/api/${userId}/tasks/stats`,
  },
} as const;

/**
 * Request/Response Headers
 */
export const API_HEADERS = {
  CONTENT_TYPE: 'Content-Type',
  AUTHORIZATION: 'Authorization',
  ACCEPT: 'Accept',
} as const;

export const CONTENT_TYPES = {
  JSON: 'application/json',
  FORM_DATA: 'multipart/form-data',
  URL_ENCODED: 'application/x-www-form-urlencoded',
} as const;
