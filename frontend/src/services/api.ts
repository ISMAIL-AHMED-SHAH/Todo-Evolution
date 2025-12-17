/**
 * Base API service for authenticated requests
 */

// Base API URL from environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Define types for our API responses
export interface User {
  id: number;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface TaskCompletionUpdate {
  completed: boolean;
}

// API service class
class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Helper method to get auth headers
  private getAuthHeaders(): Record<string, string> {
    const token = localStorage.getItem('auth_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  // Helper method to make requests
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const response = await fetch(url, {
      headers: this.getAuthHeaders(),
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Authentication methods
  async signup(email: string, password: string): Promise<User> {
    return this.request('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async signin(email: string, password: string): Promise<{ access_token: string; token_type: string }> {
    return this.request('/auth/signin', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async getProfile(): Promise<User> {
    return this.request('/auth/profile');
  }

  async logout(): Promise<{ message: string; user_id: number }> {
    return this.request('/auth/logout', {
      method: 'POST',
    });
  }

  // Task methods
  async getTasks(userId: number): Promise<Task[]> {
    return this.request(`/${userId}/tasks`);
  }

  async createTask(userId: number, taskData: TaskCreate): Promise<Task> {
    return this.request(`/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async getTask(userId: number, taskId: number): Promise<Task> {
    return this.request(`/${userId}/tasks/${taskId}`);
  }

  async updateTask(userId: number, taskId: number, taskData: TaskUpdate): Promise<Task> {
    return this.request(`/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(userId: number, taskId: number): Promise<Task> {
    return this.request(`/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async updateTaskCompletion(userId: number, taskId: number, completed: boolean): Promise<Task> {
    return this.request(`/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  }
}

// Export a singleton instance
export const apiService = new ApiService();

// Export the class as well if needed
export default ApiService;