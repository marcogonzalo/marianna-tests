/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, ReactNode } from 'react';
import { User } from '../features/auth/types/client';
import {
    login as performLogin,
    logout as performLogout,
} from '@/features/auth/api';

interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const storedToken = sessionStorage.getItem('token');
    const storedUser = sessionStorage.getItem('user');

    const [token, setToken] = useState<string | null>(storedToken);
    const [user, setUser] = useState<User | null>(
        storedUser ? JSON.parse(storedUser) : null,
    );

    const storeToken = (token: string | null) => {
        console.log(token);
        setToken(token);
        if (token === null) sessionStorage.removeItem('token');
        else sessionStorage.setItem('token', token);
    };
    const storeUser = (user: User | null) => {
        console.log(user);
        setUser(user);
        if (user === null) sessionStorage.removeItem('user');
        else sessionStorage.setItem('user', JSON.stringify(user));
    };

    const login = async (email: string, password: string) => {
        const response = await performLogin({
            username: email,
            password: password,
        });
        storeToken(response.accessToken);
        storeUser({ email: response.email });
    };

    const logout = async () => {
        try {
            if (token) {
                await performLogout(token);
            }
        } finally {
            storeToken(null);
            storeUser(null);
        }
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
