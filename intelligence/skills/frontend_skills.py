"""
Frontend Implementation Skills

Skills for generating and working with Next.js + Better Auth frontend code.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path


class FrontendSkills:
    """Skills for Next.js + Better Auth frontend implementation."""

    def __init__(self, frontend_root: Optional[Path] = None):
        """
        Initialize frontend skills.

        Args:
            frontend_root: Root directory for frontend code (defaults to ./frontend)
        """
        self.frontend_root = frontend_root or Path("frontend")

    def generate_nextjs_routes(
        self,
        pages: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """
        Generate Next.js page components.

        Args:
            pages: List of page definitions with name and route

        Returns:
            Dictionary of filename: code

        Example:
            >>> skills = FrontendSkills()
            >>> pages = skills.generate_nextjs_routes([
            ...     {"name": "Tasks", "route": "/tasks"}
            ... ])
        """
        generated_pages = {}

        for page in pages:
            name = page["name"]
            route = page["route"]

            filename = self._route_to_filename(route)
            code = self._generate_page_component(name, route)

            generated_pages[filename] = code

        return generated_pages

    def auth_ui_components(self) -> Dict[str, str]:
        """
        Generate authentication UI components.

        Returns:
            Dictionary of component_name: code

        Example:
            >>> skills = FrontendSkills()
            >>> components = skills.auth_ui_components()
        """
        return {
            "SignupForm": self._generate_signup_form(),
            "SigninForm": self._generate_signin_form(),
            "AuthButton": self._generate_auth_button(),
            "ProtectedRoute": self._generate_protected_route(),
        }

    def create_frontend_api_client(self, base_url: str = "http://localhost:8000") -> str:
        """
        Generate frontend API client for backend communication.

        Args:
            base_url: Backend API base URL

        Returns:
            API client code

        Example:
            >>> skills = FrontendSkills()
            >>> client = skills.create_frontend_api_client()
        """
        return f'''/**
 * API Client for Backend Communication
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "{base_url}";

export class ApiClient {{
    private baseUrl: string;

    constructor(baseUrl: string = API_BASE_URL) {{
        this.baseUrl = baseUrl;
    }}

    private async request<T>(
        endpoint: string,
        options: RequestInit = {{}}
    ): Promise<T> {{
        const token = this.getToken();

        const headers = {{
            "Content-Type": "application/json",
            ...(token && {{ Authorization: `Bearer ${{token}}` }}),
            ...options.headers,
        }};

        const response = await fetch(`${{this.baseUrl}}${{endpoint}}`, {{
            ...options,
            headers,
        }});

        if (!response.ok) {{
            const error = await response.json().catch(() => ({{
                message: response.statusText
            }}));
            throw new Error(error.message || `Request failed: ${{response.status}}`);
        }}

        return response.json();
    }}

    private getToken(): string | null {{
        if (typeof window === "undefined") return null;
        return localStorage.getItem("auth_token");
    }}

    private setToken(token: string): void {{
        if (typeof window === "undefined") return;
        localStorage.setItem("auth_token", token);
    }}

    private clearToken(): void {{
        if (typeof window === "undefined") return;
        localStorage.removeItem("auth_token");
    }}

    // Authentication methods
    async signup(email: string, password: string): Promise<{{ token: string }}> {{
        const result = await this.request<{{ token: string }}>("/auth/signup", {{
            method: "POST",
            body: JSON.stringify({{ email, password }}),
        }});

        this.setToken(result.token);
        return result;
    }}

    async signin(email: string, password: string): Promise<{{ token: string }}> {{
        const result = await this.request<{{ token: string }}>("/auth/signin", {{
            method: "POST",
            body: JSON.stringify({{ email, password }}),
        }});

        this.setToken(result.token);
        return result;
    }}

    async signout(): Promise<void> {{
        this.clearToken();
    }}

    // Task methods
    async getTasks(userId: number): Promise<any[]> {{
        return this.request<any[]>(`/api/${{userId}}/tasks`);
    }}

    async createTask(userId: number, task: any): Promise<any> {{
        return this.request<any>(`/api/${{userId}}/tasks`, {{
            method: "POST",
            body: JSON.stringify(task),
        }});
    }}

    async updateTask(userId: number, taskId: number, updates: any): Promise<any> {{
        return this.request<any>(`/api/${{userId}}/tasks/${{taskId}}`, {{
            method: "PUT",
            body: JSON.stringify(updates),
        }});
    }}

    async deleteTask(userId: number, taskId: number): Promise<any> {{
        return this.request<any>(`/api/${{userId}}/tasks/${{taskId}}`, {{
            method: "DELETE",
        }});
    }}

    async toggleTaskComplete(
        userId: number,
        taskId: number,
        completed: boolean
    ): Promise<any> {{
        return this.request<any>(`/api/${{userId}}/tasks/${{taskId}}/complete`, {{
            method: "PATCH",
            body: JSON.stringify({{ completed }}),
        }});
    }}
}}

export const apiClient = new ApiClient();
'''

    def connect_to_fastapi_api(self, endpoints: List[Dict[str, str]]) -> str:
        """
        Generate TypeScript service for FastAPI endpoints.

        Args:
            endpoints: List of endpoint definitions

        Returns:
            TypeScript service code
        """
        return '''/**
 * Task Service - FastAPI Integration
 */

import { apiClient } from "./api-client";

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

export class TaskService {
    async listTasks(userId: number): Promise<Task[]> {
        return apiClient.getTasks(userId);
    }

    async getTask(userId: number, taskId: number): Promise<Task> {
        return apiClient.request<Task>(`/api/${userId}/tasks/${taskId}`);
    }

    async createTask(userId: number, task: TaskCreate): Promise<Task> {
        return apiClient.createTask(userId, task);
    }

    async updateTask(
        userId: number,
        taskId: number,
        updates: TaskUpdate
    ): Promise<Task> {
        return apiClient.updateTask(userId, taskId, updates);
    }

    async deleteTask(userId: number, taskId: number): Promise<Task> {
        return apiClient.deleteTask(userId, taskId);
    }

    async toggleComplete(
        userId: number,
        taskId: number,
        completed: boolean
    ): Promise<Task> {
        return apiClient.toggleTaskComplete(userId, taskId, completed);
    }
}

export const taskService = new TaskService();
'''

    def _route_to_filename(self, route: str) -> str:
        """Convert route to Next.js filename."""
        if route == "/":
            return "page.tsx"

        # Remove leading slash and replace with path
        parts = route.strip("/").split("/")

        # Handle dynamic routes
        filename_parts = []
        for part in parts:
            if part.startswith("{") and part.endswith("}"):
                # Convert {id} to [id]
                filename_parts.append(f"[{part[1:-1]}]")
            else:
                filename_parts.append(part)

        return "/".join(filename_parts) + "/page.tsx"

    def _generate_page_component(self, name: str, route: str) -> str:
        """Generate Next.js page component."""
        return f'''/**
 * {name} Page
 */

"use client";

import {{ useEffect, useState }} from "react";
import {{ useRouter }} from "next/navigation";

export default function {name}Page() {{
    const router = useRouter();
    const [loading, setLoading] = useState(true);

    useEffect(() => {{
        // TODO: Add page initialization logic
        setLoading(false);
    }}, []);

    if (loading) {{
        return <div className="flex items-center justify-center min-h-screen">
            <p>Loading...</p>
        </div>;
    }}

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">{name}</h1>
            {{/* TODO: Add page content */}}
        </div>
    );
}}
'''

    def _generate_signup_form(self) -> str:
        """Generate signup form component."""
        return '''/**
 * Signup Form Component
 */

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "../services/api-client";

export default function SignupForm() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            await apiClient.signup(email, password);
            router.push("/tasks");
        } catch (err: any) {
            setError(err.message || "Signup failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-6">Sign Up</h2>

            {error && (
                <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                    {error}
                </div>
            )}

            <div className="mb-4">
                <label htmlFor="email" className="block text-sm font-medium mb-2">
                    Email
                </label>
                <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>

            <div className="mb-6">
                <label htmlFor="password" className="block text-sm font-medium mb-2">
                    Password
                </label>
                <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    minLength={8}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>

            <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 disabled:bg-gray-400"
            >
                {loading ? "Signing up..." : "Sign Up"}
            </button>
        </form>
    );
}
'''

    def _generate_signin_form(self) -> str:
        """Generate signin form component."""
        return '''/**
 * Signin Form Component
 */

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "../services/api-client";

export default function SigninForm() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            await apiClient.signin(email, password);
            router.push("/tasks");
        } catch (err: any) {
            setError(err.message || "Sign in failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-6">Sign In</h2>

            {error && (
                <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                    {error}
                </div>
            )}

            <div className="mb-4">
                <label htmlFor="email" className="block text-sm font-medium mb-2">
                    Email
                </label>
                <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>

            <div className="mb-6">
                <label htmlFor="password" className="block text-sm font-medium mb-2">
                    Password
                </label>
                <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>

            <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 disabled:bg-gray-400"
            >
                {loading ? "Signing in..." : "Sign In"}
            </button>
        </form>
    );
}
'''

    def _generate_auth_button(self) -> str:
        """Generate authentication button component."""
        return '''/**
 * Auth Button Component
 */

"use client";

import { useRouter } from "next/navigation";
import { apiClient } from "../services/api-client";

export default function AuthButton({ isAuthenticated }: { isAuthenticated: boolean }) {
    const router = useRouter();

    const handleSignout = async () => {
        await apiClient.signout();
        router.push("/signin");
    };

    if (!isAuthenticated) {
        return (
            <div className="flex gap-2">
                <button
                    onClick={() => router.push("/signin")}
                    className="px-4 py-2 text-blue-500 border border-blue-500 rounded-md hover:bg-blue-50"
                >
                    Sign In
                </button>
                <button
                    onClick={() => router.push("/signup")}
                    className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                >
                    Sign Up
                </button>
            </div>
        );
    }

    return (
        <button
            onClick={handleSignout}
            className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600"
        >
            Sign Out
        </button>
    );
}
'''

    def _generate_protected_route(self) -> str:
        """Generate protected route wrapper component."""
        return '''/**
 * Protected Route Wrapper
 */

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
    const router = useRouter();
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("auth_token");

        if (!token) {
            router.push("/signin");
            return;
        }

        // TODO: Verify token validity
        setIsAuthenticated(true);
        setLoading(false);
    }, [router]);

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <p>Loading...</p>
            </div>
        );
    }

    if (!isAuthenticated) {
        return null;
    }

    return <>{children}</>;
}
'''
