import { UserRole } from './shared';

export interface UserAPI {
    id: string;
    email: string;
    created_at: string;
    updated_at: string;
    deleted_at?: string;
    account?: AccountAPI;
}

export interface UserAPIRequest {
    email: string;
    password: string;
    account?: AccountAPIRequest;
}

export interface AccountAPI {
    id: string;
    first_name: string;
    last_name: string;
    role: UserRole;
    user_id: string;
    created_at: string;
    updated_at: string;
}

export interface AccountAPIRequest {
    first_name: string;
    last_name: string;
    role: UserRole;
}

export interface UserUpdateAPI {
    email?: string;
    account?: AccountAPIRequest;
}
