export interface LoginCredentials {
    username: string;
    password: string;
}

export interface AuthResponse {
    accessToken: string;
    tokenType: string;
    email: string;
}

export interface User {
    email: string;
}
