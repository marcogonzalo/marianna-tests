import { UserRole } from './shared';

export interface User {
    id: string;
    email: string;
    createdAt: string;
    updatedAt: string;
    deletedAt?: string;
    account?: Account;
}

export interface Account {
    id: string;
    firstName: string;
    lastName: string;
    role: UserRole;
    userId?: string;
    createdAt?: string;
    updatedAt?: string;
}

export interface CreateUserRequest {
    email: string;
    password: string;
    account?: CreateAccountRequest;
}

export interface UpdateUserRequest {
    email?: string;
    firstName?: string;
    lastName?: string;
    role?: UserRole;
}

export interface CreateAccountRequest {
    firstName: string;
    lastName: string;
    role: UserRole;
}
