export interface LoginCredentialsAPI {
    username: string;
    password: string;
}

export interface AuthResponseAPI {
    access_token: string;
    token_type: string;
    email: string;
}

export interface UserAPI {
    email: string;
}
