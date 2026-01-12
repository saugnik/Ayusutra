/**
 * Authentication Service
 * Handles user registration, login, and token management
 */

import apiClient from './api';
import { UserCreate, UserLogin, TokenResponse, User } from '../types/api.types';

class AuthService {
    /**
     * Register a new user
     */
    async register(userData: UserCreate): Promise<User> {
        const response = await apiClient.post<User>('/auth/register', userData);
        return response.data;
    }

    /**
     * Login user and store token
     */
    async login(credentials: UserLogin): Promise<TokenResponse> {
        const response = await apiClient.post<TokenResponse>('/auth/login', credentials);
        const tokenData = response.data;

        // Store token and user info in localStorage
        localStorage.setItem('access_token', tokenData.access_token);
        localStorage.setItem('user', JSON.stringify({
            id: tokenData.user_id,
            role: tokenData.role,
            full_name: tokenData.full_name
        }));

        return tokenData;
    }

    /**
     * Logout user
     */
    logout(): void {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
    }

    /**
     * Get current user information
     */
    async getCurrentUser(): Promise<User> {
        const response = await apiClient.get<User>('/auth/me');
        return response.data;
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated(): boolean {
        return !!localStorage.getItem('access_token');
    }

    /**
     * Get stored user info
     */
    getStoredUser(): { id: number; role: string; full_name: string } | null {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    }

    /**
     * Get access token
     */
    getToken(): string | null {
        return localStorage.getItem('access_token');
    }
}

export default new AuthService();
