export interface LoginCredentials {
    username: string;
    password: string;
}

export interface AuthResponse {
    accessToken: string;
    tokenType: string;
    email: string;
}

export interface Account {
    id: string;
    firstName: string;
    lastName: string;
    role: string;
    userId?: string;
    createdAt?: string;
    updatedAt?: string;
}

export interface User {
    id: string;
    email: string;
    createdAt: string;
    updatedAt: string;
    deletedAt?: string;
    account?: Account;
}

