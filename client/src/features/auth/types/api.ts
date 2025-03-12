export interface LoginCredentialsAPI {
    username: string;
    password: string;
}

export interface AuthResponseAPI {
    access_token: string;
    token_type: string;
    email: string;
}

export interface AccountAPI {
    id: string;
    first_name: string;
    last_name: string;
    role: string;
    user_id: string;
    created_at: string;
    updated_at: string;
}

export interface UserAPI {
    id: string;
    email: string;
    created_at: string;
    updated_at: string;
    deleted_at?: string;
    account?: AccountAPI;
}
