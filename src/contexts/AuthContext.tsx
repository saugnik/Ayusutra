/**
 * Authentication Context
 * Provides global authentication state and methods
 */

import React, { createContext, useState, useEffect, ReactNode } from 'react';
import authService from '../services/auth.service';
import { User, UserLogin, UserCreate, TokenResponse } from '../types/api.types';

interface AuthContextType {
    user: { id: number; role: string; full_name: string } | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (credentials: UserLogin) => Promise<TokenResponse>;
    register: (userData: UserCreate) => Promise<User>;
    logout: () => void;
    refreshUser: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<{ id: number; role: string; full_name: string } | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const storedUser = authService.getStoredUser();
        if (storedUser) {
            setUser(storedUser);
        }
        setIsLoading(false);
    }, []);

    const login = async (credentials: UserLogin): Promise<TokenResponse> => {
        const tokenData = await authService.login(credentials);
        setUser({
            id: tokenData.user_id,
            role: tokenData.role,
            full_name: tokenData.full_name
        });
        return tokenData;
    };

    const register = async (userData: UserCreate): Promise<User> => {
        const user = await authService.register(userData);
        return user;
    };

    const logout = () => {
        authService.logout();
        setUser(null);
    };

    const refreshUser = async () => {
        try {
            const currentUser = await authService.getCurrentUser();
            setUser({
                id: currentUser.id,
                role: currentUser.role,
                full_name: currentUser.full_name
            });
        } catch (error) {
            logout();
        }
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated: !!user,
                isLoading,
                login,
                register,
                logout,
                refreshUser
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};
